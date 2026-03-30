"""Remote test script - Working with tasks and the platform.

This demonstrates the full workflow for remote evaluations:

1. Deploy your environment to hud.ai (New -> Environment -> Connect GitHub repo)
2. Tasks are defined in tasks.py using scenario.task()
3. Run evaluations locally or at scale

## Option A: Run on Platform

Run evaluations at scale directly on hud.ai with parallel execution and automatic tracing.

## Option B: CLI Evaluation

    # Run all tasks
    hud eval my-org/blank-tasks --model gpt-4o --remote

## Option C: Python Script (this file)

    # Run all tasks locally
    python remote_test.py

    # Upload tasks to platform
    python remote_test.py --upload my-org/blank-tasks


Run the backend first: uvicorn backend.app:app --port 8005
"""

import argparse
import asyncio

import hud
from hud.agents import OpenAIChatAgent
from hud.datasets import save_tasks
from hud.eval.task import Task

from tasks import ALL_TASKS

ENV_NAME = "blank"


async def test_all_tasks():
    """Run all locally defined tasks."""
    print(f"=== Running {len(ALL_TASKS)} tasks ===")

    task_list = list(ALL_TASKS.values())

    async with hud.eval(task_list) as ctx:
        agent = OpenAIChatAgent.create(model="gpt-4o")
        await agent.run(ctx)


async def upload_to_platform(slug: str):
    """Upload tasks to the platform."""
    print(f"=== Upload to Platform: {slug} ===")

    remote_tasks = [
        Task(
            env={"name": ENV_NAME},
            scenario=f"{ENV_NAME}:{task.scenario}",
            args=task.args,
            slug=task.slug,
        )
        for task in ALL_TASKS.values()
    ]
    save_tasks(slug, remote_tasks)
    print(f"Saved {len(remote_tasks)} tasks -> hud eval {slug} --model gpt-4o")


async def main():
    parser = argparse.ArgumentParser(description="Remote task operations")
    parser.add_argument(
        "--upload",
        metavar="SLUG",
        help="Upload tasks to platform (e.g. my-org/blank-tasks)",
    )
    args = parser.parse_args()

    if args.upload:
        await upload_to_platform(args.upload)
    else:
        await test_all_tasks()


if __name__ == "__main__":
    asyncio.run(main())
