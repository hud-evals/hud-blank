# Blank Environment

A minimal counter-based HUD environment template.

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
Run it (needs OPENAI_API_KEY or HUD_API_KEY):

```python
import hud
from hud.agents import OpenAIChatAgent

async with hud.eval(tasks) as ctx:
    agent = OpenAIChatAgent.create(model="gpt-5-mini")
    await agent.run(ctx)
```
## Deploy

```bash
hud deploy
```
## Docs

Full documentation: [docs.hud.ai](https://docs.hud.ai)
