"""Blank HUD environment — a text-reasoning task and a tool-using task.

A minimal v6 template to copy from. It shows the two core pieces in the
smallest useful form:

  * ``@env.template`` — a task: yield a prompt, receive the agent's answer,
    yield a reward (here a plain float, 0.0–1.0).
  * an in-process MCP **capability** — the v6 way to expose agent-facing tools:
    a FastMCP server started in ``@env.initialize`` and registered with
    ``env.add_capability``. The calculator tools live there.

``count-letters`` is pure reasoning; ``evaluate-expression`` drives the
calculator tools. In v6 tools are exposed env-wide rather than hidden per-task,
so the reasoning task simply ignores them.
"""

import asyncio
import contextlib
import socket

from hud import Environment
from hud.capabilities import Capability

env = Environment(name="blank")

# In-memory calculator state. HUD runs one container per evaluation, so a single
# module-global instance is safe (no in-process parallelism).
_state = {"value": 0}


def _reset() -> None:
    _state["value"] = 0


# ---------------------------------------------------------------------------
# Agent-facing tools (registered on the in-process MCP server in @env.initialize)
# ---------------------------------------------------------------------------
async def add(n: int) -> str:
    """Add n to the current value."""
    _state["value"] += n
    return f"Value: {_state['value']}"


async def subtract(n: int) -> str:
    """Subtract n from the current value."""
    _state["value"] -= n
    return f"Value: {_state['value']}"


async def multiply(n: int) -> str:
    """Multiply the current value by n."""
    _state["value"] *= n
    return f"Value: {_state['value']}"


async def get_value() -> str:
    """Get the current value."""
    return f"Value: {_state['value']}"


# ---------------------------------------------------------------------------
# In-process MCP capability: serve the calculator tools to the agent
# ---------------------------------------------------------------------------
_MCP_PORT: int = 0
_MCP_SERVER_TASK: "asyncio.Task | None" = None


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


async def _listening(host: str, port: int, timeout: float = 10.0) -> None:
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while loop.time() < deadline:
        try:
            socket.create_connection((host, port), timeout=0.2).close()
            return
        except OSError:
            await asyncio.sleep(0.1)
    raise RuntimeError(f"calculator MCP server never came up on {host}:{port}")


@env.initialize
async def _up() -> None:
    # Lazy import so collecting tasks (import tasks) stays free of fastmcp noise.
    from fastmcp import FastMCP

    global _MCP_PORT, _MCP_SERVER_TASK
    if _MCP_SERVER_TASK is None:
        server = FastMCP(name="calculator")
        server.tool(add)
        server.tool(subtract)
        server.tool(multiply)
        server.tool(get_value)
        _MCP_PORT = _free_port()
        _MCP_SERVER_TASK = asyncio.create_task(
            server.run_async(transport="http", host="127.0.0.1", port=_MCP_PORT, show_banner=False)
        )
        await _listening("127.0.0.1", _MCP_PORT)
    env.add_capability(Capability.mcp(name="calculator", url=f"http://127.0.0.1:{_MCP_PORT}/mcp"))


@env.shutdown
async def _down() -> None:
    global _MCP_SERVER_TASK
    if _MCP_SERVER_TASK is not None:
        _MCP_SERVER_TASK.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await _MCP_SERVER_TASK
        _MCP_SERVER_TASK = None
    _reset()


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
@env.template(id="count-letters")
async def count_letters(word: str = "strawberry", letter: str = "r"):
    """Count how many times a letter appears in a word — pure text reasoning.

    Reward: 1.0 if the agent's answer contains the correct count, else 0.0.
    """
    answer = yield f"How many '{letter}' in '{word}'?"
    correct = str(word.lower().count(letter.lower()))
    yield 1.0 if answer and correct in answer else 0.0


@env.template(id="evaluate-expression")
async def evaluate_expression(expression: str = "3 + 2 * 3", expected: int = 9):
    """Compute a math expression using the calculator tools.

    The value starts at 0; the agent uses add/subtract/multiply/get_value to
    reach the answer. Reward: 1.0 if the final value equals ``expected``.
    """
    _reset()
    yield (
        f"Compute the result of: {expression}\n"
        f"Use the add, subtract, multiply, and get_value tools to arrive at the answer. "
        f"The value starts at 0."
    )
    yield 1.0 if _state["value"] == expected else 0.0


if __name__ == "__main__":
    # No-model smoke: boot a task's generator directly and print the reward.
    async def _smoke() -> None:
        gen = count_letters.func(word="strawberry", letter="r")
        print(await gen.asend(None))
        print("reward:", await gen.asend("there are 3"))

    asyncio.run(_smoke())
