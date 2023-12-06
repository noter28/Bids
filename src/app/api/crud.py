from app.db import client, osr, bids, database
import datetime
from sqlalchemy.dialects.postgresql import insert



async def join(payload):
    # inserted_values = []
    # client_leiCodes = []
    dict_payload = [item.dict() for item in payload]
    # dict_payload = [item.client.dict() for item in payload]

    print(dict_payload)
    # for i in payload:
    #     print(i.dict())

    # for i in range(len(payload)):
    #     inserted_values.append({'name': payload[i].client.name, 'leiCode': payload[i].client.leiCode})
    #     client_leiCodes.append(payload[i].client.leiCode)

    # print(inserted_values)
    insert_stmt = insert(client).values(
        [{'name': item['client']['name'], 'leiCode': item['client']['leiCode']} for item in dict_payload])
    on_conflict_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=['leiCode']
    )
    await database.fetch_all(query=on_conflict_stmt)
    subquery = await database.fetch_all(client.select().with_only_columns([client.c.id, client.c.leiCode]).
                                        where(
        client.c.leiCode.in_([item['client']['leiCode'] for item in dict_payload])))

    b = []
    for i in subquery:
        b.append(dict(i._mapping))
    print('TODO')
    print([{'id': item['client']['name']} for item in dict_payload])
    # print(next(item['id'] for item in b if item["leiCode"] == "25522104"))
    print([item['id'] for item in b if item['leiCode'] == "25522104"])
    a = []
    for i in payload:
        payload = i
        a.append({
            # 'clientName': payload.client.name,
            'clientLeiCode': payload.client.leiCode,
            # clientType=payload.client.clientType,
            'beginDate': datetime.datetime.strptime(payload.beginDate, "%Y-%m-%d").date(),
            'osrName': payload.distributionCombinations[0]['osr']['name'],
            # osrLeiCode=payload.distributionCombinations[0]['osr']['leiCode'],
            'ONE_A': int(payload.osrDistributions[0]['volume']),
            'ONE_B': int(payload.osrDistributions[1]['volume']),
            'TWO_A': int(payload.osrDistributions[2]['volume']),
            'TWO_B': int(payload.osrDistributions[3]['volume']),
            'client_id': next(item['id'] for item in b if item['leiCode'] == payload.client.leiCode)
        })
    print(a)

        # subquery = await database.execute(client.select().where(client.c.name == 'rrrrrrrrr'))
    # print(subquery)
    query = (bids.insert().values(a))

    # query1 = osr.insert().values
    # return await database.execute(query=subquery)

    # join_condition = client.c.leiCode == bids.c.clientLeiCode
    # query = client.outerjoin(bids, join_condition).select()
    # query = await database.fetch_all(query=query)

    # outer_join_query = select([])

    # a = []
    # for i in query:
    #     a.append(dict(i._mapping))
    # print(a)
    # ins = insert(bids).values(a)
    # await database.execute(query=ins)

    # query = query.select().where(query.c.clientLeiCode == payload.client.leiCode)
    return await database.fetch_all(query=query)


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
