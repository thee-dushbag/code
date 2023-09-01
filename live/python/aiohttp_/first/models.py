import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

metadata = sa.MetaData()
engine = sa.create_engine("sqlite:///data.sqlite3")

users = sa.Table(
    "users",
    metadata,
    sa.Column("uid", sa.Integer(), primary_key=True),
    sa.Column("username", sa.String(20), nullable=False, unique=True),
    sa.Column("password", sa.String(20), nullable=False),
    sa.Column("email", sa.Integer(), unique=True),
)

files = sa.Table(
    "files",
    metadata,
    sa.Column("fid", sa.Integer(), primary_key=True),
    sa.Column("uid", sa.ForeignKey("users.uid")),
    sa.Column("filename", sa.String(100), unique=True),
    sa.Column("size", sa.Float()),
)

metadata.create_all(engine)

conn = engine.connect()


async def verify_login(name: str, pswd: str) -> bool:
    print(f"Verifying: {name=} {pswd=}")
    q = sa.select(users.c.password).where(users.c.username == name)
    r = conn.execute(q).all()
    print(f"Query verify: {r}")
    if r:
        return r[0][0] == pswd
    return False


async def add_user(name: str, email: str, pswd: str) -> bool:
    print(f"Adding USER: {name=} {email=} {pswd=}")
    with conn.begin() as transaction:
        try:
            q = sa.insert(users).values(username=name, password=pswd, email=email)
            conn.execute(q)
        except IntegrityError as e:
            transaction.rollback()
            return False
        else:
            transaction.commit()
            return True


async def add_file(username: str, filename: str, size: float):
    print(f"Adding FILE: {filename=} {size=}")
    q = sa.select(users.c.uid).where(users.c.username == username)
    uid = conn.execute(q).scalar()
    with conn.begin() as transaction:
        try:
            q = sa.insert(files).values(filename=filename, size=size, uid=uid)
            conn.execute(q)
        except IntegrityError as e:
            transaction.rollback()
            return False
        else:
            transaction.commit()
            return True


async def get_user_files(username: str):
    print(f"Getting files for {username}")
    cols = (files.c.filename,)
    q = (
        sa.select(*cols)
        .select_from(files.join(users))
        .where(users.c.username == username)
        .group_by(files.c.fid)
    )
    rows = conn.execute(q)
    return [row.filename for row in rows]
