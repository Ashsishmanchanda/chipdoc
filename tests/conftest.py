import pytest
from fastapi.testclient import TestClient

from datasheet_hub.api.app import app
from datasheet_hub.catalog.service import CatalogService


@pytest.fixture(scope="session")
def catalog_service():
    return CatalogService()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)

