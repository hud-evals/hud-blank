"""Blank Environment - Simple text-based evaluation scenarios.

This demonstrates:
- @env.scenario() for evaluation lifecycle (prompt -> evaluate)
- @env.tool() for agent-facing calculator tools
- exclude_tools parameter to hide tools from specific scenarios
- Parametrized scenarios that can generate many task variants
"""

import subprocess
import sys
from collections.abc import AsyncGenerator
from typing import Any

from hud import Environment

env = Environment(name="blank")

# In-memory state for calculator tools
_state = {"value": 0}


def _reset():
    _state["value"] = 0


# ---------------------------------------------------------------------------
# Tools (for evaluate-expression scenario)
# ---------------------------------------------------------------------------


@env.tool()
async def add(n: int) -> str:
    """Add n to the current value."""
    _state["value"] += n
    return f"Value: {_state['value']}"


@env.tool()
async def subtract(n: int) -> str:
    """Subtract n from the current value."""
    _state["value"] -= n
    return f"Value: {_state['value']}"


@env.tool()
async def multiply(n: int) -> str:
    """Multiply the current value by n."""
    _state["value"] *= n
    return f"Value: {_state['value']}"


@env.tool()
async def get_value() -> str:
    """Get the current value."""
    return f"Value: {_state['value']}"


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


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------


@env.scenario("count-letters", exclude_tools=["*"])
async def count_letters(
    word: str = "strawberry", letter: str = "r"
) -> AsyncGenerator[Any, str | None]:
    """Count occurrences of a letter in a word.

    Tools are excluded — this is a pure text reasoning task.
    Evaluation: binary — 1.0 if answer contains the correct count, 0.0 otherwise.
    """
    answer = yield f"How many '{letter}' in '{word}'?"
    correct = str(word.lower().count(letter.lower()))
    yield 1.0 if answer and correct in answer else 0.0


@env.scenario("evaluate-expression")
async def evaluate_expression(
    expression: str = "3 + 2 * 3", expected: int = 9
) -> AsyncGenerator[Any, str | None]:
    """Compute the value of a math expression using calculator tools.

    Tools are available: add, subtract, multiply, get_value.
    The value starts at 0. Use tools to arrive at the answer.
    Evaluation: binary — 1.0 if final value matches expected, 0.0 otherwise.
    """
    _reset()
    yield (
        f"Compute the result of: {expression}\n"
        f"Use the add, subtract, and multiply tools to arrive at the answer. "
        f"The value starts at 0."
    )
    yield 1.0 if _state["value"] == expected else 0.0


if __name__ == "__main__":
    env.run(transport="stdio")
