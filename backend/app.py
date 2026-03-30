"""FastAPI backend for the blank environment.

This provides the stateful calculator service that the environment tools interact with.
Supports arithmetic operations (add, subtract, multiply) with operation history tracking.
"""

import logging
import sys

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(name)s | %(message)s",
)

app = FastAPI(title="Blank Environment Backend")


class OpRequest(BaseModel):
    n: int


# In-memory state
_state: dict = {"value": 0, "history": []}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/act")
def act():
    """Increment the value by 1 (legacy counter endpoint)."""
    _state["value"] += 1
    _state["history"].append({"op": "act", "arg": 1, "result": _state["value"]})
    return {"count": _state["value"]}


@app.post("/add")
def add(req: OpRequest):
    """Add n to the current value."""
    _state["value"] += req.n
    _state["history"].append({"op": "add", "arg": req.n, "result": _state["value"]})
    return {"value": _state["value"]}


@app.post("/subtract")
def subtract(req: OpRequest):
    """Subtract n from the current value."""
    _state["value"] -= req.n
    _state["history"].append(
        {"op": "subtract", "arg": req.n, "result": _state["value"]}
    )
    return {"value": _state["value"]}


@app.post("/multiply")
def multiply(req: OpRequest):
    """Multiply the current value by n."""
    _state["value"] *= req.n
    _state["history"].append(
        {"op": "multiply", "arg": req.n, "result": _state["value"]}
    )
    return {"value": _state["value"]}


@app.post("/reset")
def reset():
    """Reset the value to 0 and clear history."""
    _state["value"] = 0
    _state["history"] = []
    return {"ok": True}


@app.get("/state")
def state():
    """Get the current value and operation history."""
    return {"value": _state["value"], "history": _state["history"]}
