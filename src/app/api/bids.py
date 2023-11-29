from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import BidSchema, BidDB

router = APIRouter()


@router.post("/", status_code=201)
async def create_bid(payload: BidSchema):
    client_exist = await crud.client_exist(payload)
    if not client_exist:
        client_id = await crud.client_insert(payload)
    else:
        client_id = dict(client_exist._mapping)['id']
    bid_id = await crud.bid_insert(payload, client_id)
    response_object = {
        'status': 'success',
        'message': 'Bids for OSR was successfully added',
        'data': {
            'id': bid_id,
            'clientName': payload.client.name,
            'clientLeiCode': payload.client.leiCode,
            'clientType': payload.client.clientType,
            'beginDate': payload.beginDate,
            'osrName': payload.distributionCombinations[0]['osr']['name'],
            'osrLeiCode': payload.distributionCombinations[0]['osr']['leiCode'],
            'osrDistributions': payload.osrDistributions,
        }
    }
    return response_object


# @router.get("/{id}/", response_model=NoteDB)
# async def read_note(id: int):
#     note = await crud.get(id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")
#     return note
#
#
# @router.get("/", response_model=List[NoteDB])
# async def read_all_notes():
#     return await crud.get_all()
#
#
# @router.put("/{id}/", response_model=NoteDB)
# async def update_note(id: int, payload: NoteSchema):
#     note = await crud.get(id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")
#
#     note_id = await crud.put(id, payload)
#
#     response_object = {
#         "id": note_id,
#         "title": payload.title,
#         "description": payload.description,
#     }
#     return response_object
#
#
# @router.delete("/{id}/", response_model=NoteDB)
# async def delete_note(id: int):
#     note = await crud.get(id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")
#
#     await crud.delete(id)
#
#     return note