"""Shared fixtures for hud-blank test suite."""

import pytest
import httpx

import backend.app as backend_module
from backend.app import app


@pytest.fixture(autouse=True)
def reset_backend_state():
    """Reset the backend counter to 0 before every test."""
    backend_module._count = 0
    yield
    backend_module._count = 0


@pytest.fixture
def backend_app():
    """Provide the FastAPI app instance."""
    return app


@pytest.fixture
async def async_backend_client():
    """Async HTTP client talking to the backend in-process (no real server)."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture
async def patched_env(async_backend_client, monkeypatch):
    """HUD Environment with http_client patched to use in-process backend.

    Replaces the module-level httpx.AsyncClient in env.py so that
    tool calls and scenario operations go through ASGITransport instead
    of hitting a real server on localhost:8005.
    """
    import env as env_module

    monkeypatch.setattr(env_module, "http_client", async_backend_client)
    return env_module.env
