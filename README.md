# Blank Environment

A minimal counter-based HUD environment template.

## 1. Deploy to Platform

If you haven't already, connect this repo to hud.ai:

1. Push to GitHub
2. Go to [hud.ai](https://hud.ai) → **New** → **Environment**
3. Connect your GitHub repo
4. Your environment builds automatically on each push

Once deployed, your environment is accessible by its slug (e.g., `my-org/blank`).

## 2. Define Tools and Scenarios

Tools are functions agents can call. Scenarios define the evaluation lifecycle.

```python
from hud import Environment

env = Environment(name="blank")

@env.tool()
async def act() -> str:
    """Increment the counter by 1."""
    resp = await http_client.post("/act")
    return f"Counter: {resp.json().get('count', 0)}"

@env.scenario("count-to")
async def count_to(target: int = 10):
    await http_client.post("/reset")                    # Setup
    answer = yield f"Count to {target}"                 # Prompt → agent runs
    current = (await http_client.get("/state")).json()["count"]
    yield 1.0 if current >= target else 0.0             # Reward
```

## 3. Create Tasks from Scenarios

Tasks are scenario instances with specific arguments.

**In Code:**
```python
tasks = [
    env("count-to", target=3),
    env("count-to", target=10),
]
```

**From JSON:**
```json
[
  {"env": {"name": "my-org/blank"}, "scenario": "count-to", "args": {"target": 3}},
  {"env": {"name": "my-org/blank"}, "scenario": "count-to", "args": {"target": 10}}
]
```

**On Platform:**
After deploying, create tasks from your scenarios on hud.ai. Access them by slug:
```python
from hud.datasets import load_tasks
tasks = load_tasks("my-org/blank-tasks")
```

## 4. Run Evaluations

Run tasks and see results on hud.ai. You have three options:

**On Platform:**
Run evaluations at scale directly on [hud.ai](https://hud.ai) with parallel execution and automatic tracing.

**CLI:**
```bash
hud eval ./remote_tasks.json --model gpt-4o --remote  # https://hud.ai/models
hud eval my-org/blank-tasks --model gpt-4o --remote --group 5
```

**Python:**
```python
import hud
from hud.agents import OpenAIChatAgent  # See all models: https://hud.ai/models

tasks = [env("count-to", target=3), env("count-to", target=5)]

async with hud.eval(tasks) as ctx:
    agent = OpenAIChatAgent.create(model="gpt-4o")  # Uses inference.hud.ai
    await agent.run(ctx)

# Results are automatically traced to hud.ai
```

**With Variants (A/B Testing):**
```python
async with hud.eval(tasks, variants={"model": ["gpt-4o-mini", "gpt-4o"]}, group=2) as ctx:
    agent = OpenAIChatAgent.create(model=ctx.variants["model"])
    await agent.run(ctx)
```

## Local Development

```bash
# Start the backend
uvicorn backend.app:app --port 8005 --reload

# Test locally
python local_test.py

# Test with remote tasks
python remote_test.py
```

> ⚠️ **Local runs one task at a time.** For parallel execution with multiple tasks, push and run remotely:
> ```bash
> hud push
> hud eval ./remote_tasks.json --model gpt-4o --remote --group 5
> ```

## Structure

```
hud-blank/
├── env.py              # Environment + tools + scenarios
├── backend/app.py      # FastAPI backend for state
├── local_test.py       # Local testing examples
├── remote_test.py      # Platform integration examples
├── remote_tasks.json   # Task definitions
├── Dockerfile.hud
└── pyproject.toml
```

## Documentation

Full documentation: [docs.hud.ai](https://docs.hud.ai)
