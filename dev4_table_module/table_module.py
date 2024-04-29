import abc
import datetime
from enum import StrEnum
from typing import Iterable, Any, ClassVar

from sqlalchemy import Table, UUID
from sqlalchemy import select, Engine, Row

from dev3_transaction_script import models as dev3_models
from dev3_transaction_script.money import Money


class TableModule(abc.ABC):
    _table: ClassVar[Table]

    def __init__(self, engine):
        self._engine: Engine = engine

    def get(self, item_id: UUID) -> Row:
        with self._engine.connect() as connection:
            stmt = select(self._table).where(
                self._table.c.id == item_id
            )
            return connection.execute(stmt).one()


class ProductType(StrEnum):
    WORD = "W"
    SPREADSHEET = "S"
    DATABASE = "D"


class ProductsTableModule(TableModule):
    _table = dev3_models.products

    def get_type(self, product_id: UUID) -> ProductType:
        product: Row = self.get(product_id)
        return ProductType(product.type)


class RevenueRecognitionTableModule(TableModule):
    _table = dev3_models.revenue_recognitions

    def add(self, recognitions: Iterable[dict[str, Any]]):
        with self._engine.begin() as connection:
            for recognition in recognitions:
                connection.execute(self._table.insert(), recognition)

    def recognized_revenue(self, contract_id: UUID, as_of: datetime.date) -> Money:
        with self._engine.connect() as connection:
            stmt = select(self._table).where(
                (self._table.c.contract_id == contract_id)
                & (self._table.c.date <= as_of)
            )
            revenues = connection.execute(stmt)
        return sum([Money.dollars(revenue.amount) for revenue in revenues], start=Money.dollars(0))


class ContractTableModule(TableModule):
    _table = dev3_models.contracts

    def calculate_recognitions(self, contract_id: UUID):
        contract = self.get(contract_id)
        product_type = ProductsTableModule(self._engine).get_type(contract.product_id)

        days = {
            ProductType.WORD: [0],
            ProductType.SPREADSHEET: [0, 60, 90],
            ProductType.DATABASE: [0, 30, 60],
        }.get(product_type)

        if days is None:
            raise ValueError(f"Can't calculate revenue for {product_type}")

        num_of_revenues = len(days)

        total_revenue = Money.dollars(contract.amount)
        recognized_amounts = total_revenue.allocate(num_of_revenues)

        revenues = [
            dict(
                contract_id=contract.id,
                amount=recognized_amounts[i].amount,
                date=datetime.date.today() + datetime.timedelta(days=days[i])
            )
            for i in range(num_of_revenues)
        ]

        RevenueRecognitionTableModule(self._engine).add(revenues)
