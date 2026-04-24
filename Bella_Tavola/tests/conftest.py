# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def prato_valido():
    return {"nome": "Pizza de Teste", "categoria": "pizza", "preco": 50.0}