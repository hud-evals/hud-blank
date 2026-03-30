"""Tests for the FastAPI backend endpoints."""

from starlette.testclient import TestClient


def test_health(backend_app):
    client = TestClient(backend_app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_act_increments_value(backend_app):
    client = TestClient(backend_app)
    r1 = client.post("/act")
    assert r1.status_code == 200
    assert r1.json() == {"count": 1}

    r2 = client.post("/act")
    assert r2.json() == {"count": 2}


def test_add(backend_app):
    client = TestClient(backend_app)
    resp = client.post("/add", json={"n": 5})
    assert resp.status_code == 200
    assert resp.json() == {"value": 5}

    resp = client.post("/add", json={"n": 3})
    assert resp.json() == {"value": 8}


def test_subtract(backend_app):
    client = TestClient(backend_app)
    client.post("/add", json={"n": 10})
    resp = client.post("/subtract", json={"n": 3})
    assert resp.status_code == 200
    assert resp.json() == {"value": 7}


def test_multiply(backend_app):
    client = TestClient(backend_app)
    client.post("/add", json={"n": 5})
    resp = client.post("/multiply", json={"n": 3})
    assert resp.status_code == 200
    assert resp.json() == {"value": 15}


def test_reset_clears_state(backend_app):
    client = TestClient(backend_app)
    client.post("/add", json={"n": 10})
    client.post("/multiply", json={"n": 2})

    resp = client.post("/reset")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

    state = client.get("/state")
    assert state.json() == {"value": 0, "history": []}


def test_state_returns_value_and_history(backend_app):
    client = TestClient(backend_app)
    assert client.get("/state").json() == {"value": 0, "history": []}

    client.post("/add", json={"n": 5})
    client.post("/multiply", json={"n": 3})

    state = client.get("/state").json()
    assert state["value"] == 15
    assert len(state["history"]) == 2
    assert state["history"][0] == {"op": "add", "arg": 5, "result": 5}
    assert state["history"][1] == {"op": "multiply", "arg": 3, "result": 15}


def test_act_records_history(backend_app):
    client = TestClient(backend_app)
    client.post("/act")
    client.post("/act")

    state = client.get("/state").json()
    assert state["value"] == 2
    assert len(state["history"]) == 2
    assert state["history"][0] == {"op": "add", "arg": 1, "result": 1}
    assert state["history"][1] == {"op": "add", "arg": 1, "result": 2}
