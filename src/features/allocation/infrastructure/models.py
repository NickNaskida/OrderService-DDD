from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import registry


mapper_registry = registry()

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

products = Table(
    "products",
    mapper_registry.metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

batches = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", ForeignKey("products.sku")),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)
