import json

import pytest

from api import crud, schemes
from api.db import db

request_json = json.load(open("./tests/data/requests.json"))


@pytest.fixture
def company_info():
    with db():
        request = crud.request.create(schemes.CreateRequest(data=request_json["create"]))
        request_dict = {"id": request.id, "data": request.data, "user_id": None}
        return request_dict


def test_get_requests(client, company_info):
    response = client.get("/requests")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == company_info


def test_get_request(client, company_info):
    response = client.get(f"/requests/{company_info['id']}")
    assert response.status_code == 200
    assert response.json() == company_info


def test_get_request_exception(client):
    response = client.get("/requests/1")
    assert response.status_code == 404


def test_request_update(company_info):
    with db():
        updated_info = crud.request.update(
            crud.request.get_by_id(company_info["id"]), schemes.UpdateRequest(data=request_json["update"])
        )
        updated_dict = {"id": updated_info.id, "data": updated_info.data}
        assert updated_dict["id"] == company_info["id"]
        assert updated_dict["data"] == request_json["update"]


def test_search_request(client, company_info):
    response = client.get("/requests/search/test")
    assert response.status_code == 200
    assert response.json() == company_info


def test_search_request_exception(client, company_info):
    response = client.get("/requests/search/test1")
    assert response.status_code == 404


def test_delete_request(client, company_info):
    response = client.delete(f"/requests/{company_info['id']}")
    assert response.status_code == 200
    assert response.json() == company_info
