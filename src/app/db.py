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


bids = Table(
    "bids",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("clientLeiCode", String(50)),
    Column("clientType", String(50)),
    Column("beginDate", String(50)),
    Column("osrName", String(100)),
    Column("osrLeiCode", String(100)),
    Column("ONE_A", Integer),
    Column("ONE_B", Integer),
    Column("TWO_A", Integer),
    Column("TWO_B", Integer),
    Column("totalVolume", String(100)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)


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
