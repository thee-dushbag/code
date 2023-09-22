from itertools import count
from typing import NamedTuple, Optional

import attrs
import db
import exc
from more_itertools import flatten

START_UID = 1


@attrs.define(slots=True)
class UserBundle:
    "All bundles are valid if created from the manager"
    manager: "DatabaseContentManager"
    user: db.User
    resources: list[db.Resourse]

    def _get_perm_resources(self, *perms: db.Permission):
        return [r for r in self.resources if r.permission in perms]

    @property
    def public_resources(self):
        return self._get_perm_resources(db.Permission.PUBLIC)

    @property
    def protected_resources(self):
        return self._get_perm_resources(db.Permission.PROTECTED)

    @property
    def private_resources(self):
        return self._get_perm_resources(db.Permission.PRIVATE)

    def leave_group(self, gid):
        groups = set(self.user.groups)
        groups.remove(gid)
        self.user.groups = list(groups)

    def member_of(self, gid):
        self.manager.get_group(gid)
        return gid in self.user.groups

    def join_group(self, gid: int):
        if not self.member_of(gid):
            self.user.groups.append(gid)


@attrs.define(slots=True)
class GroupBundle:
    "All bundles are valid if created from the manager"
    manager: "DatabaseContentManager"
    group: db.Group

    class UserResource(NamedTuple):
        protected: list[db.Resourse]
        public: list[db.Resourse]

    def _get_group_resources(self):
        userbuns = [self.manager.get_user_bundle(u) for u in self.group.members]
        resrcs = [
            self.UserResource(u.protected_resources, u.public_resources)
            for u in userbuns
        ]
        return resrcs

    def members(self):
        return [self.manager.get_user(u) for u in self.group.members]

    def is_member(self, uid: int):
        self.manager.get_user(uid)
        return uid in self.group.members

    def add_member(self, uid: int):
        if not self.is_member(uid):
            self.group.members.append(uid)

    @property
    def public_resources(self):
        r = [f.public for f in self._get_group_resources()]
        return list(flatten(r))

    @property
    def protected_resources(self):
        r = [f.protected for f in self._get_group_resources()]
        return list(flatten(r))

    def remove_user(self, uid):
        if not self.is_member(uid):
            return
        self.group.members.remove(uid)

    @property
    def resources(self):
        return list(flatten([self.protected_resources, self.public_resources]))


@attrs.define(slots=True)
class UserGroupBundle:
    "Do not instantiate this yourself, use the content manager"
    manager: "DatabaseContentManager"
    user_bundle: UserBundle
    group_bundles: list[GroupBundle]

    def delete_resource(self, rid: int):
        resrc = self.manager.get_resource(rid)
        if resrc.owner != self.user_bundle.user.uid:
            raise exc.DBResourceNotYours(resrc)
        self.manager.delete_resource(rid)

    def update_resource(self, rid: int, resource: str, perm=None):
        p = perm or db.Permission.PROTECTED
        resrc = self.manager.get_resource(rid)
        if resrc.owner != self.user_bundle.user.uid:
            raise exc.DBResourceNotYours(resrc)
        resrc.resource = resource
        resrc.permission = p

    def add_resource(self, resource: str, perm=None):
        p = perm or db.Permission.PROTECTED
        owner = self.user_bundle.user.uid
        resrc = db.Resourse(owner=owner, resource=resource, permission=p)
        self.manager.add_resource(resrc)

    def _filter_block_my_resources(self, resrcs):
        me = self.user_bundle.user.uid
        return [r for r in resrcs if r.owner != me]

    def _group_resources(self):
        return flatten([r.resources for r in self.group_bundles])

    def get_other_resources(self):
        grp_resrcs = self._group_resources()
        return self._filter_block_my_resources(grp_resrcs)

    def get_other_public_resources(self):
        return [
            r
            for r in self.get_other_resources()
            if r.permission == db.Permission.PUBLIC
        ]

    def get_other_protected_resources(self):
        return [
            r
            for r in self.get_other_resources()
            if r.permission == db.Permission.PROTECTED
        ]

    def get_my_resources(self):
        return self.user_bundle.resources

    def create_group(self, groupname=None, groupdesc=None):
        username = self.user_bundle.user.name
        name = groupname or f"{username}'s Group"
        desc = groupdesc or f"Group created by {username}"
        grp = db.Group(groupname=name, groupdesc=desc)
        self.manager.add_group(grp)
        grpb = self.manager.get_group_bundle(grp.gid)
        self.group_bundles.append(grpb)
        grp.members.append(self.user_bundle.user.uid)
        return grp.gid

    def leave_group(self, gid):
        target = self.manager.get_group_bundle(gid)
        if target in self.group_bundles:
            target.remove_user(self.user_bundle.user.uid)
        self.user_bundle.leave_group(gid)

    def join_group(self, gid: int):
        group = self.manager.get_group_bundle(gid)
        group.add_member(self.user_bundle.user.uid)
        self.user_bundle.join_group(gid)
        self.group_bundles.append(group)

    def is_member(self, gid):
        group = self.manager.get_group_bundle(gid)
        return group.is_member(self.user_bundle.user.uid)

    def resources(self):
        return list(flatten([self.get_my_resources(), self.get_other_resources()]))


def _get_ids(iterable):
    l = list(iterable)
    l.append(START_UID)
    return l


class DatabaseManager:
    def __init__(self, database: db.Database) -> None:
        self.db: db.Database = database
        self.gidkp = count(max(_get_ids(i.gid for i in self.db.groups)))
        self.ridkp = count(max(_get_ids(i.rid for i in self.db.resources)))
        self.uidkp = count(max(_get_ids(i.uid for i in self.db.users)))

    def _get_user(self, uid: int) -> Optional[db.User]:
        if users := self._get_users(uid):
            return users[0]

    def _get_users(self, *uids: int):
        return [user for user in self.db.users if user.uid in uids]

    def _get_user_resources(self, uid: int) -> list[db.Resourse]:
        return [resrc for resrc in self.db.resources if resrc.owner == uid]

    def _get_resource(self, rid: int):
        if found := [r for r in self.db.resources if r.rid == rid]:
            return found[0]

    def _get_user_groups(self, uid: int) -> list[db.Group]:
        return [grp for grp in self.db.groups if uid in grp.members]

    def _get_groups(self, *gids: int):
        return [grp for grp in self.db.groups if grp.gid in gids]

    def _get_group(self, gid: int):
        if grps := self._get_groups(gid):
            return grps[0]


class DatabaseContentManager(DatabaseManager):
    def add_user(self, user: db.User):
        uid = next(self.uidkp)
        user.uid = uid
        self.db.users.append(user)

    def add_group(self, grp: db.Group):
        gid = next(self.gidkp)
        grp.gid = gid
        self.db.groups.append(grp)

    def add_resource(self, resrc: db.Resourse):
        rid = next(self.ridkp)
        resrc.rid = rid
        self.db.resources.append(resrc)

    def _get_item(self, getter, item):
        if r := getter(item):
            return r
        raise exc.DBSearchNotFound(item)

    def get_resource(self, rid: int):
        return self._get_item(self._get_resource, rid)

    def get_user(self, uid: int):
        return self._get_item(self._get_user, uid)

    def get_group(self, gid: int):
        return self._get_item(self._get_group, gid)

    def delete_resource(self, rid: int):
        resrc = self.get_resource(rid)
        self.db.resources.remove(resrc)

    def delete_user(self, uid: int):
        user = self.get_user_bundle(uid)
        rids = [r.rid for r in user.resources]
        for rid in rids:
            self.delete_resource(rid)
        self.db.users.remove(user.user)

    def delete_group(self, gid: int):
        group = self.get_group(gid)
        self.db.groups.remove(group)

    def get_user_bundle(self, uid: int):
        user = self.get_user(uid)
        user_resrcs = self._get_user_resources(uid)
        return UserBundle(self, user, user_resrcs)

    def get_group_bundle(self, gid: int):
        group = self.get_group(gid)
        return GroupBundle(self, group)

    def get_usergroup_bundle(self, uid: int):
        userb = self.get_user_bundle(uid)
        groupsb = [self.get_group_bundle(g) for g in userb.user.groups]
        return UserGroupBundle(self, userb, groupsb)
