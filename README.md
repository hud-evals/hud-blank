# Blank Environment

A minimal HUD environment template to use as a starting point for building your own environments.

## Setup

```bash
uv sync
hud set HUD_API_KEY=your-key-here   # CLI auth, get one at hud.ai/project/api-keys
```

## Deploy & Run

```bash
hud deploy .                              # deploy the environment (once)
hud sync tasks <taskset-name>             # push tasks to a taskset (fast, re-run on every task change)
hud eval <taskset-name> --remote --full
```

**Iteration loop:** `hud deploy` is the slow step — run it once. After that, edit `tasks.py` and re-run `hud sync tasks` (takes seconds). Only redeploy when `env.py` or the Dockerfile changes.

See [Deploy & Go Remote](https://docs.hud.ai/building/running-at-scale) for deploy flags, secrets, and auto-deploy options.

## Scenarios

### count-letters

Count occurrences of a letter in a word. No tools — pure text reasoning.

```python
env("count-letters", word="strawberry", letter="r")
```

### evaluate-expression

Compute a math expression using calculator tools (`add`, `subtract`, `multiply`). The value starts at 0 and the agent must use the tools to arrive at the answer.

```python
env("evaluate-expression", expression="3 + 2 * 3", expected=9)
```

## Documentation

To learn more about tasks, evaluations, and running at scale see the [full docs](https://docs.hud.ai).
