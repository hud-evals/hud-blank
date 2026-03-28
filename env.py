"""Blank Environment - A minimal counter-based environment for testing.

This demonstrates:
- @env.tool() for agent-facing tools
- @env.scenario() for evaluation lifecycle (setup → prompt → evaluate)
- @env.initialize and @env.shutdown for lifecycle hooks
"""

import logging
import os
import subprocess
import sys
from typing import Any

import httpx

from hud import Environment

# Configure logging to stderr (MCP uses stdout for communication)
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
    force=True,
)
for logger_name in ["httpx", "httpcore"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Backend configuration
BACKEND_PORT = os.getenv("BACKEND_PORT", "8005")
BACKEND_URL = f"http://localhost:{BACKEND_PORT}"

# HTTP client for backend communication
http_client = httpx.AsyncClient(base_url=BACKEND_URL, timeout=10.0)

# Create the environment
env = Environment(name="blank")


@env.tool()
async def act() -> str:
    """Increment the counter by 1."""
    resp = await http_client.post("/act")
    return f"Counter: {resp.json().get('count', 0)}"


@env.tool()
async def hud_validate() -> str:
    """Run the test suite to validate the environment is working correctly."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd="/app",
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise RuntimeError(output or f"pytest exited with code {result.returncode}")
    return output


@env.scenario("count-to", exclude_tools=["hud_validate"])
async def count_to(target: int = 10) -> Any:
    """Count to a target number by calling act() repeatedly."""
    await http_client.post("/reset")

    answer = yield f"Call act() until the counter reaches {target}."

    current = (await http_client.get("/state")).json().get("count", 0)
    yield min(1.0, current / target) if target > 0 else 1.0


@env.initialize
async def init() -> None:
    """Check backend health on startup."""
    (await http_client.get("/health")).raise_for_status()


@env.shutdown
async def cleanup() -> None:
    """Close HTTP client on shutdown."""
    await http_client.aclose()


if __name__ == "__main__":
    env.run(transport="stdio")
