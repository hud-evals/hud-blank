# Blank Environment

A minimal counter-based HUD environment template.

## Deploy

1. Push this repo to GitHub
2. Go to [hud.ai](https://hud.ai) → **New** → **Environment**
3. Connect your GitHub repo — it builds automatically on each push

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
hud eval my-org/blank-tasks --model gpt-4o --remote
```

Or in Python:

```python
import hud
from hud.agents import OpenAIChatAgent

async with hud.eval(tasks) as ctx:
    agent = OpenAIChatAgent.create(model="gpt-4o")
    await agent.run(ctx)
```

## Docs

Full documentation: [docs.hud.ai](https://docs.hud.ai)
