from sqlalchemy import MetaData, UUID
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy import create_engine

metadata_obj = MetaData()

products = Table(
    "products",
    metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("name", String(16), nullable=False),
    Column("type", String(2), nullable=False),
)

contracts = Table(
    "contracts", metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("when_signed", DateTime),
    Column("amount", Numeric),
    Column("product_id", ForeignKey("products.id")),
)

revenue_recognitions = Table(
    "revenue_recognitions", metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("contract_id", ForeignKey("contracts.id")),
    Column("amount", Numeric),
    Column("date", DateTime),
)

engine = create_engine("postgresql://solvbot_test:testpgpassword@localhost:5432/solvbot_test")
metadata_obj.create_all(engine)
