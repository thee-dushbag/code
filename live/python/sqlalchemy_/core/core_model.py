import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("uid", sa.Integer(), primary_key=True),
    sa.Column("name", sa.String(30), index=True),
    sa.Column("email", sa.String(50), unique=True),
    sa.Column("age", sa.Integer(), sa.CheckConstraint("age >= 18")),
)

products = sa.Table(
    "products",
    metadata,
    sa.Column("pid", sa.Integer(), primary_key=True),
    sa.Column("name", sa.String(30), index=True),
    sa.Column("description", sa.String(255)),
    sa.Column("unit_cost", sa.Numeric(6, 2)),
    sa.Column("quantity", sa.Integer(), default=1),
)

orders = sa.Table(
    "orders",
    metadata,
    sa.Column("oid", sa.Integer(), primary_key=True),
    sa.Column("uid", sa.ForeignKey("users.uid")),
    sa.Column("pid", sa.ForeignKey("products.pid")),
    sa.Column("quantity", sa.Integer(), default=1),
)

engine = sa.create_engine("sqlite:///db_core.sqlite3")
metadata.create_all(engine)
