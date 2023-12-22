from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import BidSchema, BidDB
from typing import List
from openpyxl import Workbook
import os
import msal
import jwt
import json
import requests
from datetime import datetime

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


@router.post("/join/")
async def read_note(payload: List[BidSchema]):
    data = await crud.join(payload)
    return {
        'status': 'success',
        'message': 'Bids for OSR was successfully processed',
        'data': data
    }


@router.get("/excel/")
async def excel():
    # wb = Workbook()
    # ws = wb.active
    # ws['A3'] = 42
    # wb.save("sample2.xlsx")
    # return 'success'

    # Data for auth
    accessToken = None
    tenantID = 'e8c92bf5-2138-43f0-8e58-0c0382d2334e'
    authority = 'https://login.microsoftonline.com/' + tenantID
    clientID = 'd5918b13-ed1a-44b9-b6c3-bd08c8d209d6'
    scope = ['https://graph.microsoft.com/.default']
    thumbprint = 'BF399E409ECD6EEA08D9E389ED31D5748B16894B'
    certfile = 'server.pem'

    # Data for upload excel file
    site_id = "8b2f1519-a497-4efe-8d83-b2a1d4d15d8e"
    drive_id = 'b!GRUvi5ek_k6Ng7Kh1NFdjmu4BbllQgdHiWuZ2hmgRDm97BYuvkPkRLzzr8z5Gp3v'
    file_path = 'sample2.xlsx'
    folder_name = 'test2'
    file_name = 'sample8.xlsx'
    upload_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/root:/{folder_name}/{file_name}:/content'

    def msal_certificate_auth(clientID, scope, authority, thumbprint, certfile):
        app = msal.ConfidentialClientApplication(clientID, authority=authority,
                                                 client_credential={"thumbprint": thumbprint,
                                                                    "private_key": open(certfile).read()})
        result = app.acquire_token_for_client(scopes=scope)
        return result

    def msal_jwt_expiry(accessToken):
        decodedAccessToken = jwt.decode(accessToken, verify=False)
        tokenExpiry = datetime.fromtimestamp(int(decodedAccessToken['exp']))
        print("Token Expires at: " + str(tokenExpiry))
        return tokenExpiry
        # Auth
    try:
        if not accessToken:
            try:
                # Get a new Access Token using Client Credentials Flow and a Self Signed Certificate
                accessToken = msal_certificate_auth(clientID, scope, authority, thumbprint, certfile)
            except Exception as err:
                print('Error acquiring authorization token. Check your tenantID, clientID and certficate thumbprint.')
                print(err)
        tokenExpiry = msal_jwt_expiry(accessToken['access_token'])
        time_to_expiry = tokenExpiry - datetime.now()
        if time_to_expiry.seconds < 600:
            print("Access Token Expiring Soon. Renewing Access Token.")
            accessToken = msal_certificate_auth(clientID, scope, authority, thumbprint, certfile)

    except Exception as err:
        print(err)
    # Query
    try:
        with open(file_path, 'rb') as file:
            headers = {
                'Authorization': f"Bearer {accessToken['access_token']}",
                'Content-Type': 'application/octet-stream',
                'Content-Length': str(os.path.getsize(file_path))
            }
            response = requests.put(upload_url, headers=headers, data=file)
    except Exception as err:
        print(err)
    return response.json()


@router.post("/exist/")
async def exist(payload: List[BidSchema]):
    a = await crud.is_exist(payload)
    return a




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
