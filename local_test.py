"""Local test script for the blank environment.

Run the backend first: uvicorn backend.app:app --port 8005
Then run this script: python local_test.py
"""

import asyncio

import hud
from hud.agents import OpenAIChatAgent
from hud.settings import settings
from openai import AsyncOpenAI

from env import env

# Use HUD inference gateway - see all models at https://hud.ai/models
client = AsyncOpenAI(base_url="https://inference.hud.ai", api_key=settings.api_key)


async def test_tools_standalone():
    """Test environment tools directly."""
    print("=== Test 1: Standalone Tools ===")

    async with env:
        print(f"Tools: {[t.name for t in env.as_tools()]}")
        for _ in range(3):
            print(await env.call_tool("act"))


async def test_scenario():
    """Test scenario with manual OpenAI calls."""
    print("\n=== Test 2: Scenario (Manual Agent Loop) ===")

    task = env("count-to", target=3)

    async with hud.eval(task) as ctx:
        messages = [{"role": "user", "content": ctx.prompt}]

        while True:
            response = await client.chat.completions.create(
                model="gpt-4o",  # https://hud.ai/models
                messages=messages,
                tools=ctx.as_openai_chat_tools(),
            )
            msg = response.choices[0].message

            if not msg.tool_calls:
                break

            messages.append(msg)
            for tc in msg.tool_calls:
                result = await ctx.call_tool(tc)
                messages.append(result)


async def main():
    await test_tools_standalone()
    # Uncomment to run scenarios:
    # await test_scenario()


if __name__ == "__main__":
    asyncio.run(main())
