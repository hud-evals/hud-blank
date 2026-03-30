"""Blank Environment - A calculator-based environment for testing.

This demonstrates:
- @env.tool() for agent-facing tools (arithmetic operations)
- @env.scenario() for evaluation lifecycle (setup -> prompt -> evaluate)
- @env.initialize and @env.shutdown for lifecycle hooks
- Multiple evaluation patterns: partial credit, binary, subscores, history-based
"""

import logging
import os
import sys
from collections.abc import AsyncGenerator
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


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@env.tool()
async def act() -> str:
    """Increment the counter by 1."""
    resp = await http_client.post("/act")
    return f"Counter: {resp.json().get('count', 0)}"


@env.tool()
async def add(n: int) -> str:
    """Add n to the current value."""
    resp = await http_client.post("/add", json={"n": n})
    return f"Value: {resp.json()['value']}"


@env.tool()
async def subtract(n: int) -> str:
    """Subtract n from the current value."""
    resp = await http_client.post("/subtract", json={"n": n})
    return f"Value: {resp.json()['value']}"


@env.tool()
async def multiply(n: int) -> str:
    """Multiply the current value by n."""
    resp = await http_client.post("/multiply", json={"n": n})
    return f"Value: {resp.json()['value']}"


@env.tool()
async def get_state() -> str:
    """Get the current value and number of operations performed."""
    resp = await http_client.get("/state")
    data = resp.json()
    return f"Value: {data['value']}, Operations: {len(data['history'])}"


@env.tool()
async def reset() -> str:
    """Reset the value to 0 and clear operation history."""
    await http_client.post("/reset")
    return "Reset to 0"


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------


@env.scenario("count-to")
async def count_to(target: int = 10) -> AsyncGenerator[Any, None]:
    """Count to a target number by calling act() repeatedly.

    Evaluation: partial credit — min(1.0, current / target).
    Scores 0 if any tool other than act() is used.
    """
    await http_client.post("/reset")

    yield f"Call act() until the counter reaches {target}. Do not use any other tools."

    data = (await http_client.get("/state")).json()
    current = data.get("value", 0)
    history = data.get("history", [])

    # Fail if the agent used any tool other than act()
    if any(entry.get("op") != "act" for entry in history):
        yield 0.0
    else:
        yield min(1.0, current / target) if target > 0 else 1.0


@env.scenario("compute-expression")
async def compute_expression(
    expression: str = "2 * 3 + 4", expected: int = 10
) -> AsyncGenerator[Any, None]:
    """Compute the result of a math expression using calculator tools.

    Evaluation: binary — 1.0 if the final value matches expected, 0.0 otherwise.
    """
    await http_client.post("/reset")

    yield (
        f"Compute the result of: {expression}\n"
        f"Use the add, subtract, and multiply tools to arrive at the answer. "
        f"The value starts at 0."
    )

    current = (await http_client.get("/state")).json()["value"]
    yield 1.0 if current == expected else 0.0


# ---------------------------------------------------------------------------
# Lifecycle hooks
# ---------------------------------------------------------------------------


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
