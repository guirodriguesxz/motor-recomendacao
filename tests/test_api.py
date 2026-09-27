from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "online"}


def test_recomendar_com_historico():
    resp = client.post(
        "/api/v1/recomendar",
        json={"cliente_id": 1, "produtos_comprados": ["Corte de Cabelo Masculino"]},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["cliente_id"] == 1
    assert body["metodo_utilizado"] == "Similaridade de Cosseno"
    assert "Corte de Cabelo Masculino" not in body["produtos_recomendados"]


def test_recomendar_cliente_novo_usa_fallback():
    resp = client.post("/api/v1/recomendar", json={"cliente_id": 2, "produtos_comprados": []})
    assert resp.status_code == 200
    assert resp.json()["metodo_utilizado"] == "Popularidade (Fallback)"


def test_payload_invalido_retorna_422():
    resp = client.post("/api/v1/recomendar", json={"produtos_comprados": []})
    assert resp.status_code == 422
