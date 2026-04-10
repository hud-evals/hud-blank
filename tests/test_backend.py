"""Tests for the FastAPI backend endpoints."""

from starlette.testclient import TestClient


def test_health(backend_app):
    client = TestClient(backend_app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_act_increments_counter(backend_app):
    client = TestClient(backend_app)
    r1 = client.post("/act")
    assert r1.status_code == 200
    assert r1.json() == {"count": 1}

    r2 = client.post("/act")
    assert r2.json() == {"count": 2}


def test_reset_clears_counter(backend_app):
    client = TestClient(backend_app)
    client.post("/act")
    client.post("/act")

    resp = client.post("/reset")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

    state = client.get("/state")
    assert state.json() == {"count": 0}


def test_state_returns_current_count(backend_app):
    client = TestClient(backend_app)
    assert client.get("/state").json() == {"count": 0}

    client.post("/act")
    client.post("/act")
    client.post("/act")
    assert client.get("/state").json() == {"count": 3}
