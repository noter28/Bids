from app.db import client, osr, bids, database
import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, or_, exists


async def is_exist(payload):
    dict_payload = [item.dict() for item in payload]
    for i in dict_payload:
        # Check if bid exist
        conditions = select(
            [exists().where(bids.c.beginDate == datetime.datetime.strptime(i['beginDate'], "%Y-%m-%d").date(),
                            bids.c.clientLeiCode == i['client']['leiCode'],
                            bids.c.ONE_A == int(i['osrDistributions'][0]['volume']),
                            bids.c.ONE_B == int(i['osrDistributions'][1]['volume']),
                            bids.c.TWO_A == int(i['osrDistributions'][2]['volume']),
                            bids.c.TWO_B == int(i['osrDistributions'][3]['volume']),
                            bids.c.osrName == i['distributionCombinations'][0]['osr']['name']
                            )])
        exist = await database.execute(query=conditions)
        if exist:
            pass
        else:
            # Insert client if it's new
            insert_stmt = insert(client).values({
                'name': i['client']['name'],
                'leiCode': i['client']['leiCode']
            })
            on_conflict_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['leiCode'])
            print(111111)
            print(await database.fetch_one(query=on_conflict_stmt.returning(client.c.id)))

            # Get FK client ID for bid
            client_id_query = (client.select().with_only_columns([client.c.id])
                               .where(client.c.leiCode == i['client']['leiCode']))
            client_id = await database.execute(query=client_id_query)
            print(222222)
            print(client_id)

            # Get FK osr ID for bid
            osr_id_query = (osr.select().with_only_columns([osr.c.id])
                            .where(osr.c.name == i['distributionCombinations'][0]['osr']['name']))
            osr_id = await database.execute(query=osr_id_query)
            # Insert bid
            stmt = insert(bids).values({
                'clientLeiCode': i['client']['leiCode'],
                'beginDate': datetime.datetime.strptime(i['beginDate'], "%Y-%m-%d").date(),
                'osrName': i['distributionCombinations'][0]['osr']['name'],
                'ONE_A': int(i['osrDistributions'][0]['volume']),
                'ONE_B': int(i['osrDistributions'][1]['volume']),
                'TWO_A': int(i['osrDistributions'][2]['volume']),
                'TWO_B': int(i['osrDistributions'][3]['volume']),
                'client_id': client_id,
                'osr_id': osr_id
            })
            on_conflict_stmt = stmt.on_conflict_do_update(constraint='unique_3',
                                                          set_=dict(ONE_A=stmt.excluded.ONE_A,
                                                                    ONE_B=stmt.excluded.ONE_B,
                                                                    TWO_A=stmt.excluded.TWO_A,
                                                                    TWO_B=stmt.excluded.TWO_B)
                                                          )
            await database.execute(query=on_conflict_stmt)
            print(exist)
    return exist


async def join(payload):
    dict_payload = [item.dict() for item in payload]
    insert_stmt = insert(client).values(
        [{'name': item['client']['name'],
          'leiCode': item['client']['leiCode']} for item in dict_payload])
    on_conflict_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['leiCode'])
    await database.fetch_all(query=on_conflict_stmt)

    subquery = await database.fetch_all(client.select()
    .with_only_columns([client.c.id, client.c.leiCode])
    .where(
        client.c.leiCode.in_([item['client']['leiCode'] for item in dict_payload])))

    lei_code_id_mapping = [dict(i._mapping) for i in subquery]
    bids_rows = [{
        'clientLeiCode': i.client.leiCode,
        'beginDate': datetime.datetime.strptime(i.beginDate, "%Y-%m-%d").date(),
        'osrName': i.distributionCombinations[0]['osr']['name'],
        'ONE_A': int(i.osrDistributions[0]['volume']),
        'ONE_B': int(i.osrDistributions[1]['volume']),
        'TWO_A': int(i.osrDistributions[2]['volume']),
        'TWO_B': int(i.osrDistributions[3]['volume']),
        'client_id': next(item['id'] for item in lei_code_id_mapping if item['leiCode'] == i.client.leiCode)
    } for i in payload]
    stmt = insert(bids).values(bids_rows)
    on_update_stmt = stmt.on_conflict_do_update(constraint='unique_bid',
                                                set_=dict(ONE_A=stmt.excluded.ONE_A,
                                                          ONE_B=stmt.excluded.ONE_B,
                                                          TWO_A=stmt.excluded.TWO_A,
                                                          TWO_B=stmt.excluded.TWO_B)).returning(bids.c.id)
    return await database.fetch_all(query=on_update_stmt)


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
