# Blank Environment

Minimal starter template for building HUD environments.

## Quick Start

```bash
# Build the Docker image
hud build

# Start hot-reload development server
hud dev

# Run the sample tasks
hud eval tasks.json
```

## Deploy

When you're ready to use this environment in production:

1. Push your code to GitHub
2. Connect your repo at [hud.ai](https://hud.ai/environments/new)
3. Builds will trigger automatically on each push

## Architecture

- **`environment/`** - Owns state, exposes HTTP endpoints (`/health`, `/act`, `/reset`, `/state`)
- **`server/`** - Wraps environment in MCP tools for agents

## Learn More

For complete documentation on building environments and running evaluations, visit [docs.hud.ai](https://docs.hud.ai).