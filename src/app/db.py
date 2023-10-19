import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
# notes = Table(
#     "bids",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(50)),
#     Column("identification_number", String(50)),
#     Column("delivery_start_date", String(50)),
#     Column("delivery_end_date", String(50)),
#     Column("distribution_system_operator", String(100)),
#     Column("ordered_volumes_first_voltage_class_a", Integer),
#     Column("ordered_volumes_first_voltage_class_b", Integer),
#     Column("ordered_volumes_second_voltage_class_a", Integer),
#     Column("ordered_volumes_second_voltage_class_b", Integer),
#     Column("ordered_volumes_by_voltage_first_class", Integer),
#     Column("ordered_volumes_by_voltage_second_class", Integer),
#     Column("ordered_volumes_a", Integer),
#     Column("ordered_volumes_b", Integer),
#     Column("total", Integer),
#     Column("created_date", DateTime, default=func.now(), nullable=False),
# )

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
