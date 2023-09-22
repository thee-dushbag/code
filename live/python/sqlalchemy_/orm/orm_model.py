import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

metadata = sa.MetaData()
Base = declarative_base(metadata=metadata)
engine: sa.Engine = sa.create_engine("sqlite:///db.sqlite3", echo=False)
Session = sessionmaker(engine)


class User(Base):
    __tablename__ = "users"
    uid = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(30), index=True)
    email = sa.Column(sa.String(50), unique=True)
    age = sa.Column(sa.Integer(), sa.CheckConstraint("age >= 18"))

    @property
    def str(self) -> str:
        return f"User(uid={self.uid!r}, name={self.name!r}, email={self.email!r}, age={self.age!r})"


class Product(Base):
    __tablename__ = "products"
    pid = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(30), index=True)
    description = sa.Column(sa.String(255))
    unit_cost = sa.Column(sa.Numeric(6, 2))
    quantity = sa.Column(sa.Integer(), default=1)

    @property
    def str(self) -> str:
        return f"Product(pid={self.pid!r}, name={self.name!r}, description={self.description!r}, unit_cost={self.unit_cost!r}, quantity={self.quantity!r})"


class Order(Base):
    __tablename__ = "orders"
    oid = sa.Column(sa.Integer(), primary_key=True)
    uid = sa.Column(sa.ForeignKey("users.uid"))
    pid = sa.Column(sa.ForeignKey("products.pid"))
    quantity = sa.Column(sa.Integer(), default=1)

    @property
    def str(self) -> str:
        return f"Order(oid={self.oid!r}, uid={self.uid!r}, pid={self.pid!r}, quantity={self.quantity!r})"


metadata.create_all(engine)
