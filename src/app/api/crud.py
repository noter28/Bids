from app.db import client, osr, bids, database
import datetime
from sqlalchemy.dialects.postgresql import insert


async def join(payload):
    dict_payload = [item.dict() for item in payload]

    insert_stmt = insert(client).values(
        [{'name': item['client']['name'],
          'leiCode': item['client']['leiCode']} for item in dict_payload])
    on_conflict_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['leiCode'])
    await database.fetch_all(query=on_conflict_stmt)

    subquery = await database.fetch_all(client.select().
    with_only_columns([client.c.id, client.c.leiCode]).
    where(
        client.c.leiCode.in_([item['client']['leiCode'] for item in dict_payload])))

    lei_code_id_mapping = []
    for i in subquery:
        lei_code_id_mapping.append(dict(i._mapping))
    bids_rows = []
    for i in payload:
        payload = i
        bids_rows.append({
            'clientLeiCode': payload.client.leiCode,
            'beginDate': datetime.datetime.strptime(payload.beginDate, "%Y-%m-%d").date(),
            'osrName': payload.distributionCombinations[0]['osr']['name'],
            'ONE_A': int(payload.osrDistributions[0]['volume']),
            'ONE_B': int(payload.osrDistributions[1]['volume']),
            'TWO_A': int(payload.osrDistributions[2]['volume']),
            'TWO_B': int(payload.osrDistributions[3]['volume']),
            'client_id': next(item['id'] for item in lei_code_id_mapping if item['leiCode'] == payload.client.leiCode)
        })
    query = insert(bids).values(bids_rows).on_conflict_do_nothing(constraint='uix_1').returning(bids.c.id)
    return await database.fetch_all(query=query)
    # return [{'name': item['client']['name'],
    #          'leiCode': item['client']['leiCode']} for item in dict_payload]


async def client_exist(payload):
    fk = client.select().where(client.c.name == payload.client.name)
    return await database.fetch_one(query=fk)


async def client_insert(payload):
    return await database.execute(query=client.insert().values(
        name=payload.client.name,
        leiCode=payload.client.leiCode,
    ))


async def bid_insert(payload, client_id):
    subquery = await database.execute(client.select().where(client.c.name == 'rrrrrrrrr'))
    # print(subquery)
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
        client_id=subquery
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
