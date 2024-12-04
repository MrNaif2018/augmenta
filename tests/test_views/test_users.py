import json

import pytest

user_json = json.load(open("./tests/data/users.json"))


@pytest.fixture
def user(client):
    response = client.post("/users", json=user_json["create"])
    assert response.status_code == 200
    return response.json()


def test_create_user(user):
    assert user.items() >= user_json["get"].items()


def test_create_user_exception(client):
    response = client.post("/users", json=user_json["create"])
    assert response.status_code == 422


def test_update_user(client, user):
    response = client.patch(f"/users/{user['id']}", json=user_json["update"])
    assert response.status_code == 200
    assert response.json().items() >= user_json["get_updated"].items()


def test_get_users(client, user):
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == user


def test_get_user(client, user):
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json() == user


def test_get_user_exception(client):
    response = client.get("/users/1")
    assert response.status_code == 404


def test_delete_user(client, user):
    responce = client.delete(f"/users/{user['id']}")
    assert responce.status_code == 200
    assert responce.json() == user
