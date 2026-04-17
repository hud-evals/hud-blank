# Blank Environment

A minimal HUD environment template to use as a starting point for building your own environments.

## Quick Start

```bash
uv sync                # install dependencies
hud deploy.            # build and deploy to HUD platform
hud sync tasks <name>  # upload task definitions
```

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
