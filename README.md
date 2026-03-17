# Blank Environment

A minimal counter-based HUD environment template.

## Deploy

```bash
hud deploy
```

## How It Works

`env.py` defines a single tool (`act` — increments a counter) and a single scenario (`count-to` — evaluates whether an agent can count to a target).

```python
@env.tool()
async def act() -> str:
    """Increment the counter by 1."""

@env.scenario("count-to")
async def count_to(target: int = 10):
    """Count to a target number."""
```

## Run Evaluations

```bash
hud eval blank-tasks --model gpt-5-mini --remote
```

Or in Python:

```python
import hud
from hud.agents import OpenAIChatAgent

async with hud.eval(tasks) as ctx:
    agent = OpenAIChatAgent.create(model="gpt-5-mini")
    await agent.run(ctx)
```

## Docs

Full documentation: [docs.hud.ai](https://docs.hud.ai)
