from hud import Environment

env = Environment(name="blank")

_count = 0


@env.tool()
async def act() -> str:
    """Increment the counter by 1."""
    global _count
    _count += 1
    return f"Counter: {_count}"


@env.scenario("count-to")
async def count_to(target: int = 10):
    """Count to a target number."""
    global _count
    _count = 0
    answer = yield f"Call act() until the counter reaches {target}."
    yield min(1.0, _count / target) if target > 0 else 1.0


if __name__ == "__main__":
    env.run(transport="stdio")
