from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import BidSchema, BidDB
from typing import List
from openpyxl import Workbook
import os

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
    # import os
    # import requests
    # client_id = '416ebd45-eb82-4d4c-9a37-92f91e8e3923'
    # client_secret = 'ca9748f1-06f8-48bc-aead-99d778abe199'  # TODO check we need secret or secretID
    # tenant_id = 'e8c92bf5-2138-43f0-8e58-0c0382d2334e'
    #
    # # SharePoint Online site URL and library name
    # site_id = '8b2f1519-a497-4efe-8d83-b2a1d4d15d8e'
    # library_name = 'sridoclib'
    # drive_id = 'b!GRUvi5ek_k6Ng7Kh1NFdjmu4BbllQgdHiWuZ2hmgRDn_Z5nTjMlVSaLTuISvH2HS'
    #
    # # Authenticate and get an access token
    # auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    # data = {
    #     'grant_type': 'client_credentials',
    #     'client_id': client_id,
    #     'client_secret': client_secret,
    #     'scope': 'https://graph.microsoft.com/.default'
    # }
    # response = requests.post(auth_url, data=data)
    # print(response.json())
    # access_token = response.json()['access_token']
    #
    # # Upload a file to the SharePoint document library using the Microsoft Graph API
    # file_path = 'C:/Users/sridevi/Desktop/test.txt'  # local file path
    # file_name = 'test.txt'
    # folder_name = 'sri'
    # upload_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/root:/{folder_name}/{file_name}:/content'
    # headers = {
    #     'Authorization': f'Bearer {access_token}',
    #     'Content-Type': 'application/octet-stream',
    #     'Content-Length': str(os.path.getsize(file_path))
    # }

    import msal
    import jwt
    import json
    import sys
    import requests
    from datetime import datetime
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization

    global accessToken
    global requestHeaders
    global tokenExpiry

    accessToken = None
    requestHeaders = None
    tokenExpiry = None

    graphURI = 'https://graph.microsoft.com'
    tenantID = 'e8c92bf5-2138-43f0-8e58-0c0382d2334e'
    authority = 'https://login.microsoftonline.com/' + tenantID
    clientID = 'd5918b13-ed1a-44b9-b6c3-bd08c8d209d6'
    scope = ['https://graph.microsoft.com/.default']
    thumbprint = 'BF399E409ECD6EEA08D9E389ED31D5748B16894B'
    certfile = 'server.pem'
    queryUser = "pryshliakoi@dteksecdev.onmicrosoft.com"

    def msal_certificate_auth(clientID, scope, authority, thumbprint, certfile):
        app = msal.ConfidentialClientApplication(clientID, authority=authority,
                                                 client_credential={"thumbprint": thumbprint,
                                                                    "private_key": open(certfile).read()})
        result = app.acquire_token_for_client(scopes=scope)
        return result

    def msgraph_request(resource, requestHeaders):
        # Request
        results = requests.get(resource, headers=requestHeaders).json()
        return results

    def msal_jwt_expiry(accessToken):
        decodedAccessToken = jwt.decode(accessToken, verify=False)  # , algorithms=["RS256"]
        accessTokenFormatted = json.dumps(decodedAccessToken, indent=2)

        # Token Expiry
        tokenExpiry = datetime.fromtimestamp(int(decodedAccessToken['exp']))
        print("Token Expires at: " + str(tokenExpiry))
        return tokenExpiry

        # Auth

    try:
        if not accessToken:
            try:
                # print(open(certfile).read())
                # Get a new Access Token using Client Credentials Flow and a Self Signed Certificate
                accessToken = msal_certificate_auth(clientID, scope, authority, thumbprint, certfile)
                requestHeaders = {
                    'Authorization': 'Bearer ' + accessToken['access_token']}
            except Exception as err:
                print('Error acquiring authorization token. Check your tenantID, clientID and certficate thumbprint.')
                print(err)
        if accessToken:
            # Example of checking token expiry time to expire in the next 10 minutes
            decodedAccessToken = jwt.decode(accessToken['access_token'], verify=False)
            accessTokenFormatted = json.dumps(decodedAccessToken, indent=2)
            print("Decoded Access Token")
            print(accessTokenFormatted)

            # Token Expiry
            tokenExpiry = msal_jwt_expiry(accessToken['access_token'])
            now = datetime.now()
            time_to_expiry = tokenExpiry - now

            if time_to_expiry.seconds < 600:
                print("Access Token Expiring Soon. Renewing Access Token.")
                accessToken = msal_certificate_auth(clientID, scope, authority, thumbprint, certfile)
                requestHeaders = {'Authorization': 'Bearer ' + accessToken['access_token']}
            else:
                minutesToExpiry = time_to_expiry.seconds / 60
                print("Access Token Expires in '" + str(minutesToExpiry) + " minutes'")

    except Exception as err:
        print(err)

    # Query
    if requestHeaders and accessToken:
        print(6)
        # queryResults = msgraph_request(graphURI + '/beta/users/' + queryUser, requestHeaders)
        print(7)
        try:
            print(8)
            # print(json.dumps(queryResults, indent=2))
            print(9)
        except Exception as err:
            print(err)

    headers = {
        'Authorization': f"Bearer {accessToken}",
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json"
    }
    site_id = "8b2f1519-a497-4efe-8d83-b2a1d4d15d8e"
    item_id = '8b2f1519-a497-4efe-8d83-b2a1d4d15d8e,b905b86b-4265-4707-896b-99da19a04439'
    drive_id = 'b!GRUvi5ek_k6Ng7Kh1NFdjmu4BbllQgdHiWuZ2hmgRDm97BYuvkPkRLzzr8z5Gp3v'
    list_id = '1'
    filename = 'test'
    sharepoint_base_url = 'https://dteksecdev.sharepoint.com/sites/DSO/SitePages'
    # sharepoint_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists"
    # 2e16ecbd-43be-44e4-bcf3-afccf91a9def
    sharepoint_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/2e16ecbd-43be-44e4-bcf3-afccf91a9def"

    response = requests.get(url=sharepoint_url, headers=requestHeaders)
    print(response.content)
    file_path = 'sample2.xlsx'
    folder_name = 'test2'
    file_name = 'sample3.xlsx'
    upload_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/root:/{folder_name}/{file_name}:/content'
    headers = {
        'Authorization': f"Bearer {accessToken['access_token']}",
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(os.path.getsize(file_path))
    }

    with open(file_path, 'rb') as file:
        response = requests.put(upload_url, headers=headers, data=file)
        print(response.json())


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
