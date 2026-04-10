# Blank Environment

A minimal HUD environment template with two parametrized scenarios.

## 1. Deploy to Platform

If you haven't already, connect this repo to hud.ai:

1. Push to GitHub
2. Go to [hud.ai](https://hud.ai) → **New** → **Environment**
3. Connect your GitHub repo
4. Your environment builds automatically on each push

Once deployed, your environment is accessible by its slug (e.g., `my-org/blank`).

## 2. Scenarios

### count-letters (no tools)

Count occurrences of a letter in a word. Pure text reasoning — no tools available.

```python
@env.scenario("count-letters", exclude_tools=["*"])
async def count_letters(word: str = "strawberry", letter: str = "r"):
    answer = yield f"How many '{letter}' in '{word}'?"
    correct = str(word.lower().count(letter.lower()))
    yield 1.0 if answer and correct in answer else 0.0
```

### evaluate-expression (with tools)

Compute a math expression using calculator tools (add, subtract, multiply).

```python
@env.scenario("evaluate-expression")
async def evaluate_expression(expression: str = "3 + 2 * 3", expected: int = 9):
    _reset()
    yield f"Compute: {expression}. Use add/subtract/multiply tools. Value starts at 0."
    yield 1.0 if _state["value"] == expected else 0.0
```

## 3. Create Tasks from Scenarios

Tasks are scenario instances with specific arguments.

**In Code:**
```python
tasks = [
    env("count-letters", word="strawberry", letter="r"),
    env("count-letters", word="mississippi", letter="s"),
    env("evaluate-expression", expression="3 + 2 * 3", expected=9),
]
```

**From JSON:**
```json
[
  {"env": {"name": "my-org/blank"}, "scenario": "count-letters", "args": {"word": "strawberry", "letter": "r"}},
  {"env": {"name": "my-org/blank"}, "scenario": "evaluate-expression", "args": {"expression": "3 + 2 * 3", "expected": 9}}
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
hud eval ./remote.json --model gpt-4o --remote
hud eval my-org/blank-tasks --model gpt-4o --remote --group 5
```

**Python:**
```python
import hud
from hud.agents import OpenAIChatAgent

tasks = [env("count-letters", word="strawberry", letter="r")]

async with hud.eval(tasks) as ctx:
    agent = OpenAIChatAgent.create(model="gpt-4o")
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
# List available tasks
python local_test.py --list

# Run a task locally
python local_test.py --task count_r_strawberry
python local_test.py --task eval_order_of_ops --model gpt-4o

# Test with remote tasks
python remote_test.py
```

## Structure

```
hud-blank/
├── env.py              # Environment + tools + scenarios
├── tasks.py            # Sample task instances
├── local_test.py       # Local testing script
├── remote_test.py      # Platform integration examples
├── remote.json         # Example task definition
├── Dockerfile.hud
└── pyproject.toml
```

## Documentation

Full documentation: [docs.hud.ai](https://docs.hud.ai)
