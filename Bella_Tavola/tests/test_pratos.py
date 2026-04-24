from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_pratos_retorna_200():
    response = client.get("/pratos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_prato_inexistente_retorna_404():
    response = client.get("/pratos/9999")
    assert response.status_code == 404

def test_criar_prato_invalido_retorna_422():
    response = client.post("/pratos", json={"nome": "X", "preco": -10})
    assert response.status_code == 422