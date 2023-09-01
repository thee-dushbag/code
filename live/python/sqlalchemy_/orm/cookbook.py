from dataclasses import asdict
from typing import Sequence
import sqlalchemy as sa
from typing import Type
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    DeclarativeBase,
)
from sqlalchemy.ext.hybrid import (
    hybrid_method,
    hybrid_property
)
from db_orm_data import product_, sample_products


ENGINE_PATH = 'sqlite:///cookbook.sqlite3'
metadata = sa.MetaData()
Base: Type[DeclarativeBase] = declarative_base(metadata=metadata)
engine = sa.create_engine(ENGINE_PATH)
Session = sessionmaker(bind=engine)
session = Session()


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

    @hybrid_property
    def instock_price(self):
        print("Computing Instock Price")
        return self.unit_cost * self.quantity

    @hybrid_method
    def add_more(self, quantity: int):
        print("Checking if more products should be added")
        return self.quantity + quantity


metadata.create_all(engine)


def init(products: Sequence[product_]):
    session.add_all(Product(**asdict(prod)) for prod in products)
    session.commit()


def main(argv: Sequence[str]) -> None:
    # init(sample_products)
    print(Product.instock_price < 67)
    print(Product.add_more(45))
    prod = session.query(Product).where(Product.pid == 1).one()
    print(prod.instock_price)
    print(prod.add_more(4))


if __name__ == '__main__':
    from sys import argv
    main(argv[1:])