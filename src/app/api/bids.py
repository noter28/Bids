from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import BidSchema
from .auth import auth
from .excel_ops import write_excel, generate_excel_file
from typing import List


file_path = 'ОЕМ_  реестр_листопад.xlsx'
site_id = "8b2f1519-a497-4efe-8d83-b2a1d4d15d8e"
drive_id = 'b!GRUvi5ek_k6Ng7Kh1NFdjmu4BbllQgdHiWuZ2hmgRDm97BYuvkPkRLzzr8z5Gp3v'
folder_name = 'test2'
file_name = 'sample8.xlsx'
upload_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/root:/{folder_name}/{file_name}:/content'


router = APIRouter()


@router.post('/all_in_one/')
async def all(payload: List[BidSchema]):
    list_of_changed_DSO = await crud.is_exist(payload)
    for DSO in list_of_changed_DSO:  # list_of_changed_DSO = [[name1, date1], [name2, date2]]
        data = await crud.get_month_data(DSO['beginDate'], DSO['osr_name'])
        print(data)
        await generate_excel_file(data, DSO['link_to_template'])
    accessToken = await auth()
    await write_excel(accessToken, file_path, upload_url)
    return list_of_changed_DSO
