from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    leiCode: str
    name: str
    clientType: str


class BidSchema(BaseModel):
    client: Client
    beginDate: str
    distributionCombinations: list
    osrDistributions: list


class BidDB(BidSchema):
    id: int
