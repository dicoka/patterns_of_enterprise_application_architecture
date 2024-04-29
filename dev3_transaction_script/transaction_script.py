import datetime
from typing import Iterable, Any

from sqlalchemy import select, Engine, Row

from dev3_transaction_script import models as dev3_models
from dev3_transaction_script.money import Money


class Gateway:
    def __init__(self, engine: Engine):
        self.engine = engine

    def find_contract(self, product_id: int) -> Row:
        with self.engine.connect() as connection:
            table = dev3_models.contracts
            stmt = select(table).where(
                table.c.id == product_id
            )
            return connection.execute(stmt).one()

    def find_recognitions_for(self, contract_id: int, as_of: datetime.date) -> Iterable[Row]:
        with self.engine.connect() as connection:
            table = dev3_models.revenue_recognitions
            stmt = select(table).where(
                (table.c.contract_id == contract_id)
                & (table.c.date <= as_of)
            )
            return connection.execute(stmt)

    def insert_recognitions(self, recognitions: list[dict[str, Any]]):
        with self.engine.connect() as connection:
            table = dev3_models.revenue_recognitions
            for recognition in recognitions:
                connection.execute(
                    table.insert().values(**recognition)
                )


class RecognitionService:
    def recognized_revenue(self, contract_id: int, as_of_date: datetime.date) -> Money:
        gateway = Gateway(dev3_models.engine)
        revenues = gateway.find_recognitions_for(contract_id, as_of_date)
        return sum([Money.dollars(revenue.amount) for revenue in revenues], start=Money.dollars(0))

    def calculate_revenue_recognitions(self, contract_id: int):
        gateway = Gateway(dev3_models.engine)
        contract: Row = gateway.find_contract(contract_id)
        total_revenue: Money = Money.dollars(contract.amount)

        if contract.type == "W":
            days = [0]
        elif contract.type == "S":
            days = [0, 60, 90]
        elif contract.type == "D":
            days = [0, 30, 60]
        else:
            raise ValueError(f"Can't calculate revenue for {contract.type}")

        num_of_revenues = len(days)
        allocated = total_revenue.allocate(num_of_revenues)

        revenues = [
            dict(
                contract_id=contract.id,
                amount=allocated[i].amount,
                date=datetime.date.today() + datetime.timedelta(days=days[i])
            )
            for i in range(num_of_revenues)
        ]

        gateway.insert_recognitions(revenues)
