"""Tests for the blank environment scenarios."""

# pyright: reportArgumentType=false

import asyncio

from env import (
    _reset,
    _state,
    add,
    count_letters,
    evaluate_expression,
    multiply,
    subtract,
)


def run(coro):
    """Helper to run async code in tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


class TestCountLetters:
    """Tests for the count-letters scenario."""

    def test_strawberry_r(self):
        async def _test():
            gen = count_letters(word="strawberry", letter="r")
            prompt = await gen.asend(None)
            assert prompt == "How many 'r' in 'strawberry'?"
            reward = await gen.asend("There are 3 r's")
            assert reward == 1.0

        run(_test())

    def test_strawberry_r_wrong(self):
        async def _test():
            gen = count_letters(word="strawberry", letter="r")
            await gen.asend(None)
            reward = await gen.asend("There are 2 r's")
            assert reward == 0.0

        run(_test())

    def test_mississippi_s(self):
        async def _test():
            gen = count_letters(word="mississippi", letter="s")
            prompt = await gen.asend(None)
            assert prompt == "How many 's' in 'mississippi'?"
            reward = await gen.asend("4")
            assert reward == 1.0

        run(_test())

    def test_case_insensitive(self):
        async def _test():
            gen = count_letters(word="BANANA", letter="a")
            await gen.asend(None)
            reward = await gen.asend("3")
            assert reward == 1.0

        run(_test())

    def test_no_matches(self):
        async def _test():
            gen = count_letters(word="hello", letter="z")
            await gen.asend(None)
            reward = await gen.asend("0")
            assert reward == 1.0

        run(_test())


class TestEvaluateExpression:
    """Tests for the evaluate-expression scenario."""

    def test_correct_result(self):
        async def _test():
            gen = evaluate_expression(expression="3 + 2 * 3", expected=9)
            prompt = await gen.asend(None)
            assert "3 + 2 * 3" in prompt
            # Simulate agent computing 3 + 2*3 = 9
            # Start at 0, add 2, multiply by 3 (=6), add 3 (=9)
            await add(2)
            await multiply(3)  # value = 6
            await add(3)  # value = 9
            reward = await gen.asend("Done")
            assert reward == 1.0

        run(_test())

    def test_wrong_result(self):
        async def _test():
            gen = evaluate_expression(expression="5 + 5", expected=10)
            await gen.asend(None)
            await add(5)  # Only added once, value = 5
            reward = await gen.asend("Done")
            assert reward == 0.0

        run(_test())

    def test_reset_between_scenarios(self):
        async def _test():
            # First scenario
            gen1 = evaluate_expression(expression="2 + 2", expected=4)
            await gen1.asend(None)
            await add(4)
            reward1 = await gen1.asend("Done")
            assert reward1 == 1.0
            assert _state["value"] == 4

            # Second scenario should reset
            gen2 = evaluate_expression(expression="3 + 3", expected=6)
            await gen2.asend(None)
            assert _state["value"] == 0  # Should be reset
            await add(6)
            reward2 = await gen2.asend("Done")
            assert reward2 == 1.0

        run(_test())


class TestCalculatorTools:
    """Tests for the calculator tools."""

    def setup_method(self):
        _reset()

    def test_add(self):
        async def _test():
            result = await add(5)
            assert result == "Value: 5"
            assert _state["value"] == 5

        run(_test())

    def test_subtract(self):
        async def _test():
            _state["value"] = 10
            result = await subtract(3)
            assert result == "Value: 7"
            assert _state["value"] == 7

        run(_test())

    def test_multiply(self):
        async def _test():
            _state["value"] = 5
            result = await multiply(3)
            assert result == "Value: 15"
            assert _state["value"] == 15

        run(_test())

    def test_chained_operations(self):
        async def _test():
            await add(5)
            await multiply(2)
            await subtract(3)
            assert _state["value"] == 7

        run(_test())
