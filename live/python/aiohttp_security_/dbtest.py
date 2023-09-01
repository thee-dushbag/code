import db, db_utils
import atexit
from random import choice
from pathlib import Path
from faker import Faker
fake = Faker()
from mpack import print

DELETE = 0

def create_user():
    p = fake.password()
    n = fake.first_name().lower()
    e = fake.email()
    return db.User(email=e, name=n, password=p)

db_file = Path('user_group_resrc.json')
perms = [db.Permission(i) for i in range(1, 4)]

if db_file.exists() and DELETE: db_file.unlink()

database = db.load_database(db_file)
atexit.register(db.save_database, database, db_file)
manager = db_utils.DatabaseContentManager(database)

def add_users(users):
    for u in users:
        manager.add_user(u)

def create_resources(rids: int, usrbundles):
    for _ in range(rids):
        user = choice(usrbundles)
        r = fake.sentence(4, False)
        p = choice(perms)
        user.add_resource(r, p)

def create_groups(n, user_bundles):
    gids = []
    for _ in range(n):
        user = choice(user_bundles)
        g = user.create_group()
        gids.append(g)
    return gids

def add_user_to_groups(m: int, userbundles, gids):
    c, t = 0, 0
    while c < m:
        t += 1
        user = choice(userbundles)
        gid = choice(gids)
        if user.is_member(gid):
            if t > m * 3: break
            else: continue
        user.join_group(gid)
        c += 1

# users = [create_user() for _ in range(7)]
# add_users(users)
# user_group_bundle = [manager.get_usergroup_bundle(u.uid) for u in users]
# create_resources(20, user_group_bundle)
# gids = create_groups(10, user_group_bundle)
# add_user_to_groups(10, user_group_bundle, gids)

users = [manager.get_usergroup_bundle(u.uid) for u in database.users]
for user in users:
    print(f"details on {user.user_bundle.user.name.upper()}:")
    print(user)
    print(list(user.resources()))