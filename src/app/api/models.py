from pydantic import BaseModel


class Client(BaseModel):
    leiCode: str
    name: str
    clientType: str


class BidSchema(BaseModel):
    client: Client
    totalVolume: str
    beginDate: str
    distributionCombinations: list
    osrDistributions: list


class NoteSchema(BaseModel):
    title: str
    description: str


class BidDB(BidSchema):
    id: int

class NoteDB(NoteSchema):
    id: int