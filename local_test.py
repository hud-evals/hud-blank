"""Local test script for the blank environment.

Run the backend first: uvicorn backend.app:app --port 8005

Usage:
    python local_test.py --list
    python local_test.py --task count_to_3
    python local_test.py --task reach_efficient_100 --model gpt-4o
"""

import argparse
import asyncio

import hud
from hud.agents import OpenAIChatAgent

from tasks import ALL_TASKS


async def main():
    available = sorted(ALL_TASKS)

    parser = argparse.ArgumentParser(description="Run agent against a blank env task")
    parser.add_argument("--task", default="count_to_3", choices=available)
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--max-steps", type=int, default=20)
    parser.add_argument(
        "--list", action="store_true", help="List available tasks and exit"
    )
    args = parser.parse_args()

    if args.list:
        for t in available:
            print(t)
        return

    task = ALL_TASKS[args.task]

    print(f"=== {args.task} ({args.model}) ===")
    async with hud.eval(task, name=args.task) as ctx:
        agent = OpenAIChatAgent.create(model=args.model)
        await agent.run(ctx, max_steps=args.max_steps)
        print(f"Reward: {ctx.reward}")


if __name__ == "__main__":
    asyncio.run(main())
