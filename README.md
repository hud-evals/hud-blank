# Blank Environment (HUD v6)

A minimal HUD v6 environment to copy from. It shows the two core pieces in
the smallest useful form:

- **`count-letters`** — a pure text-reasoning task (`@env.template`): yield a
  prompt, score the agent's answer.
- **`evaluate-expression`** — a tool-using task: the agent drives calculator
  tools (`add`, `subtract`, `multiply`, `get_value`) exposed as an in-process
  MCP **capability**.

## Setup

```bash
uv sync                              # install deps into a local venv
hud set HUD_API_KEY=your-key-here    # get one at hud.ai/project/api-keys
```

## Run a local eval

The task runs on your machine; the model is called through the HUD gateway:

```bash
hud eval tasks.py claude --task-ids count-r-strawberry --group 3
```

Pick any task slug from `tasks.py` (`count-r-strawberry`, `eval-order-of-ops`, …),
any model from `hud models list`, and any agent type (`claude`, `openai`, `gemini`, `openai_compatible`).
Add `--full` to run every task in the dataset.

## Local development

```bash
hud serve env:env        # serve the environment locally
uv run python env.py     # no-model smoke: boot a task, print the reward
```

## Tests

```bash
uv run pytest tests/
```

Offline unit tests covering both templates (`count-letters`, `evaluate-expression`),
the calculator tools, and the served `mcp` capability. No model, gateway, or live
keys are called.

## Deploy & run remotely

```bash
hud deploy .                         # build + deploy the image (slow; run once)
hud sync tasks blank                 # push tasks to a taskset (fast; re-run on task edits)
hud eval blank --remote --full       # run on the platform
```

**Iteration loop:** `hud deploy` is the slow step. After it, editing `tasks.py`
only needs `hud sync tasks`. Redeploy only when `env.py` or the Dockerfile change.

## How it works

A task is an async generator that yields twice: first the **prompt**, then the
**reward** (a float 0.0–1.0). Agent-facing tools are exposed as an MCP capability
— a FastMCP server started in `@env.initialize` and registered via
`env.add_capability`. In v6 a template can't hide tools per-task, so the
calculator is available env-wide; `count-letters` simply ignores it.

| File | Role |
|------|------|
| `env.py` | The environment: the two templates + the calculator MCP capability. Entry point (`hud serve env:env`). |
| `tasks.py` | Concrete task rows for `hud eval` / `hud sync tasks`. |
| `pyproject.toml` | Dependencies + uv config (drives `uv sync`, `uv run pytest`). |
| `Dockerfile.hud` | Image built by `hud deploy`; `uv sync`s deps and serves `env:env`. |
| `tests/` | Unit tests for the templates + tools. |

## Documentation

See the [HUD docs](https://docs.hud.ai) for tasks, capabilities, and running at scale.
