from fastapi import FastAPI

from app.api import bids, ping
from app.db import engine, database, metadata

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)
app.include_router(bids.router, prefix="/bids", tags=["bids"])
