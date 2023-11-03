from app.api.models import NoteSchema, BidSchema
from app.db import notes, bids, database


async def post(payload: BidSchema):
    query = bids.insert().values(name=payload.client.name,
                                 clientLeiCode=payload.client.leiCode,
                                 clientType=payload.client.clientType,
                                 beginDate=payload.beginDate,
                                 osrName=payload.distributionCombinations[0]['osr']['name'],
                                 osrLeiCode=payload.distributionCombinations[0]['osr']['leiCode'],
                                 # ONE_A=payload.distributionCombinations[0]['powerClassAndGroups']['ONE_A'],
                                 # ONE_B=payload.distributionCombinations[0]['powerClassAndGroups']['ONE_B'],
                                 # TWO_A=payload.distributionCombinations[0]['powerClassAndGroups']['TWO_A'],
                                 # TWO_B=payload.distributionCombinations[0]['powerClassAndGroups']['TWO_B'],
                                 totalVolume=payload.totalVolume
                                 )
    return await database.execute(query=query)


async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = bids.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: NoteSchema):
    query = (
        notes
        .update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)

