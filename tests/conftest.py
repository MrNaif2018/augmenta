import pytest
from fastapi.testclient import TestClient

from api.db import db
from main import get_app


@pytest.fixture
def app():
    return get_app()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture(autouse=True)
def init_db(app):
    db.drop_all(confirmed=True)
    db.create_all()
    yield
