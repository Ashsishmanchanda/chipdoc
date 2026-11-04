import pytest
from fastapi.testclient import TestClient

from chipdoc.api.app import app
from chipdoc.catalog.service import CatalogService


@pytest.fixture(scope="session")
def catalog_service():
    return CatalogService()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)

