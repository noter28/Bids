import os

from sqlalchemy import (
    Column,
    DateTime,
    Date,
    Integer,
    MetaData,
    String,
    Table,
    ForeignKey,
    create_engine,
    text
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
    Column("beginDate", Date),
    Column("ONE_A", Integer),
    Column("ONE_B", Integer),
    Column("TWO_A", Integer),
    Column("TWO_B", Integer),
    Column("clientLeiCode", String(50)),
    Column("clientLeiCode", String(50)),
    Column("created_date", DateTime, server_default=func.now(), nullable=False),
    Column('last_updated', DateTime, nullable=True),
    # Column("client_id", Integer, ForeignKey("client.client_id"), nullable=False),
)


osr = Table(
    "osr",
    metadata,
    Column("osr_id", Integer, primary_key=True),
    Column("osrName", String(100)),
    Column("osrLeiCode", String(100)),
    Column("created_date", DateTime, server_default=func.now(), nullable=False),
    Column("updated_date", DateTime, onupdate=func.now(), nullable=False),
)


client = Table(
    "client",
    metadata,
    Column("client_id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("clientLeiCode", String(50)),
    Column("clientType", String(50)),
    Column("created_date", DateTime, server_default=func.now(), nullable=False),
    Column("updated_date", DateTime, onupdate=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
