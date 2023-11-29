from app.api.models import BidSchema
from app.db import client, osr, bids, database
import datetime


# async def post(payload: BidSchema):
#     fk = client.select().where(client.c.name == payload.client.name)
#     client_exist = await database.fetch_one(query=fk)
#     if not client_exist:
#         client_id = await database.execute(query=client.insert().values(
#             name=payload.client.name,
#             leiCode=payload.client.leiCode,
#         ))
#     else:
#         client_id = dict(client_exist._mapping)['id']
#     query = bids.insert().values(
#                                  # clientName=payload.client.name,
#                                  clientLeiCode=payload.client.leiCode,
#                                  # clientType=payload.client.clientType,
#                                  beginDate=datetime.datetime.strptime(payload.beginDate, "%Y-%m-%d").date(),
#                                  osrName=payload.distributionCombinations[0]['osr']['name'],
#                                  # osrLeiCode=payload.distributionCombinations[0]['osr']['leiCode'],
#                                  ONE_A=int(payload.osrDistributions[0]['volume']),
#                                  ONE_B=int(payload.osrDistributions[1]['volume']),
#                                  TWO_A=int(payload.osrDistributions[2]['volume']),
#                                  TWO_B=int(payload.osrDistributions[3]['volume']),
#                                  client_id=client_id
#                                  )
#     # query1 = osr.insert().values
#     return await database.execute(query=query)


# async def join_and_merge(payload):
#     join_condition = client.c.leiCode == bids.c.clientLeiCode
#     query = client.join(bids, join_condition)
#     join_result = await database.fetchall(query=query)
#     insert_stmt = client.insert().values(
#         join_result
#     )
#
#     return await database.execute(query=insert_stmt.on_conflict_do_update(
#         constraint='pk_my_table',
#         index_elements=['leiCode'],
#         # set={}
#     ))


async def client_exist(payload):
    fk = client.select().where(client.c.name == payload.client.name)
    return await database.fetch_one(query=fk)


async def client_insert(payload):
    return await database.execute(query=client.insert().values(
        name=payload.client.name,
        leiCode=payload.client.leiCode,
    ))


async def bid_insert(payload, client_id):
    query = bids.insert().values(
        # clientName=payload.client.name,
        clientLeiCode=payload.client.leiCode,
        # clientType=payload.client.clientType,
        beginDate=datetime.datetime.strptime(payload.beginDate, "%Y-%m-%d").date(),
        osrName=payload.distributionCombinations[0]['osr']['name'],
        # osrLeiCode=payload.distributionCombinations[0]['osr']['leiCode'],
        ONE_A=int(payload.osrDistributions[0]['volume']),
        ONE_B=int(payload.osrDistributions[1]['volume']),
        TWO_A=int(payload.osrDistributions[2]['volume']),
        TWO_B=int(payload.osrDistributions[3]['volume']),
        client_id=client_id
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

