import os
from sqlalchemy import (
    Column,
    UniqueConstraint,
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
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("beginDate", Date, nullable=False),
    Column("ONE_A", Integer),
    Column("ONE_B", Integer),
    Column("TWO_A", Integer),
    Column("TWO_B", Integer),
    Column("clientLeiCode", String(50), nullable=False),
    Column("osrName", String(50), nullable=False),
    Column("created_date", DateTime, server_default=func.now(), nullable=False),
    Column('last_updated', DateTime, nullable=True),
    Column("client_id", Integer, ForeignKey("client.id"), nullable=False),
    UniqueConstraint('beginDate', 'ONE_A', 'ONE_B', 'TWO_A', 'TWO_B', 'clientLeiCode', 'osrName', name='uix_1'),
)


osr = Table(
    "osr",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("leiCode", String(100), unique=True),
    Column("created_date", DateTime, server_default=func.now(), nullable=False),
    Column("last_updated", DateTime, onupdate=func.now(), nullable=True),
)


client = Table(
    "client",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("leiCode", String(50), unique=True),
    Column("created_date", DateTime, server_default=func.now(), nullable=False),
    Column("last_updated", DateTime, onupdate=func.now(), nullable=True),
)

# databases query builder
database = Database(DATABASE_URL)
