import json

import pytest

from app.api import crud


def test_create_bid(test_app, monkeypatch):
    test_request_payload = {
        "client": {
            "leiCode": "25522107",
            "name": "ТОВ \"Агро-Овен\"",
            "clientType": "CONSUMER"
        },
        "totalVolume": "4280000",
        "beginDate": "2023-08-01",
        "distributionCombinations": [
            {
                "osr": {
                    "name": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                    "leiCode": "TODO"
                },
                "powerClassAndGroups": [
                    "ONE_A",
                    "ONE_B",
                    "TWO_A",
                    "TWO_B"
                ]
            }
        ],
        "osrDistributions": [
            {
                "osrId": "TODO",
                "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                "powerClassAndGroup": "ONE_A",
                "volume": "0"
            },
            {
                "osrId": "TODO",
                "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                "powerClassAndGroup": "ONE_B",
                "volume": 2380000
            },
            {
                "osrId": "TODO",
                "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                "powerClassAndGroup": "TWO_A",
                "volume": 0
            },
            {
                "osrId": "TODO",
                "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                "powerClassAndGroup": "TWO_B",
                "volume": 1900000
            }
        ]
    }
    test_response_payload = {
        "status": "success",
        "message": "Bids for OSR was successfully added",
        "data": {
            "id": 1,
            "clientName": "ТОВ \"Агро-Овен\"",
            "clientLeiCode": "25522107",
            "clientType": "CONSUMER",
            "beginDate": "2023-08-01",
            "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
            "osrLeiCode": "TODO",
            "osrDistributions": [
                {
                    "osrId": "TODO",
                    "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                    "powerClassAndGroup": "ONE_A",
                    "volume": "0"
                },
                {
                    "osrId": "TODO",
                    "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                    "powerClassAndGroup": "ONE_B",
                    "volume": 2380000
                },
                {
                    "osrId": "TODO",
                    "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                    "powerClassAndGroup": "TWO_A",
                    "volume": 0
                },
                {
                    "osrId": "TODO",
                    "osrName": "АТ «ДТЕК ДНІПРОВСЬКІ ЕЛЕКТРОМЕРЕЖІ»",
                    "powerClassAndGroup": "TWO_B",
                    "volume": 1900000
                }
            ]
        }
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/bids/", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/bids/", content=json.dumps({"title": "something"}))
    assert response.status_code == 422
