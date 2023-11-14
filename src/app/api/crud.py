from app.api.models import BidSchema
from app.db import osr, bids, database


async def post(payload: BidSchema):
    query = bids.insert().values(
                                 # clientName=payload.client.name,
                                 # clientLeiCode=payload.client.leiCode,
                                 # clientType=payload.client.clientType,
                                 beginDate=payload.beginDate,
                                 # osrName=payload.distributionCombinations[0]['osr']['name'],
                                 # osrLeiCode=payload.distributionCombinations[0]['osr']['leiCode'],
                                 ONE_A=int(payload.osrDistributions[0]['volume']),
                                 ONE_B=int(payload.osrDistributions[1]['volume']),
                                 TWO_A=int(payload.osrDistributions[2]['volume']),
                                 TWO_B=int(payload.osrDistributions[3]['volume']),
                                 )
    # query1 = osr.insert().values
    return await database.execute(query=query)


# async def get(id: int):
#     query = notes.select().where(id == notes.c.id)
#     return await database.fetch_one(query=query)
#
#
# async def get_all():
#     query = bids.select()
#     return await database.fetch_all(query=query)
#
#
# async def put(id: int, payload: NoteSchema):
#     query = (
#         notes
#         .update()
#         .where(id == notes.c.id)
#         .values(title=payload.title, description=payload.description)
#         .returning(notes.c.id)
#     )
#     return await database.execute(query=query)
#
#
# async def delete(id: int):
#     query = notes.delete().where(id == notes.c.id)
#     return await database.execute(query=query)

