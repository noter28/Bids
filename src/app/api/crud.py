from app.db import client, osr, bids, database
import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, or_, exists


async def is_exist(payload):
    """
    Write data (client, bids) to DB if not exist
    :param payload:
    :return: list of changed DSO
    """
    dict_payload = [item.dict() for item in payload]
    list_of_changed_DSO = []
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
            print(await database.fetch_one(query=on_conflict_stmt.returning(client.c.id)))

            # Get FK client ID for bid
            client_id_query = (client.select().with_only_columns([client.c.id])
                               .where(client.c.leiCode == i['client']['leiCode']))
            client_id = await database.execute(query=client_id_query)

            # Get FK osr ID for bid
            osr_query = (osr.select().with_only_columns([osr.c.id, osr.c.link_to_template])
                            .where(osr.c.name == i['distributionCombinations'][0]['osr']['name']))
            osr_data = await database.fetch_one(query=osr_query)

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
                'osr_id': osr_data['id']
            })
            on_conflict_stmt = stmt.on_conflict_do_update(constraint='unique_3',
                                                          set_=dict(ONE_A=stmt.excluded.ONE_A,
                                                                    ONE_B=stmt.excluded.ONE_B,
                                                                    TWO_A=stmt.excluded.TWO_A,
                                                                    TWO_B=stmt.excluded.TWO_B)
                                                          )
            await database.execute(query=on_conflict_stmt)
            list_of_changed_DSO.append({'beginDate': i['beginDate'],
                                        'osr_name': i['distributionCombinations'][0]['osr']['name'],
                                        'link_to_template': osr_data['link_to_template']})
    return list_of_changed_DSO


# Function that returns data for one DSO
# begind date, OSR

async def get_month_data(beginDate, OSR):
    beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%d").date()
    data = bids.select().where(bids.c.beginDate == beginDate,
                               bids.c.osr_id == osr.select().with_only_columns([osr.c.id])
                               .where(osr.c.name == OSR))
    data = await database.fetch_all(query=data)
    return data
