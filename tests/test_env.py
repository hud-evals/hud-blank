"""Tests for the blank env: calculator tools, task templates, and the served capability."""

# pyright: reportArgumentType=false

from env import (
    _reset,
    _state,
    add,
    count_letters,
    env,
    evaluate_expression,
    multiply,
    subtract,
)


class TestCountLetters:
    """The count-letters task."""

    async def test_strawberry_r(self):
        gen = count_letters.func(word="strawberry", letter="r")
        prompt = await gen.asend(None)
        assert prompt == "How many 'r' in 'strawberry'?"
        reward = await gen.asend("There are 3 r's")
        assert reward == 1.0

    async def test_strawberry_r_wrong(self):
        gen = count_letters.func(word="strawberry", letter="r")
        await gen.asend(None)
        reward = await gen.asend("There are 2 r's")
        assert reward == 0.0

    async def test_mississippi_s(self):
        gen = count_letters.func(word="mississippi", letter="s")
        prompt = await gen.asend(None)
        assert prompt == "How many 's' in 'mississippi'?"
        reward = await gen.asend("4")
        assert reward == 1.0

    async def test_case_insensitive(self):
        gen = count_letters.func(word="BANANA", letter="a")
        await gen.asend(None)
        reward = await gen.asend("3")
        assert reward == 1.0

    async def test_no_matches(self):
        gen = count_letters.func(word="hello", letter="z")
        await gen.asend(None)
        reward = await gen.asend("0")
        assert reward == 1.0


class TestEvaluateExpression:
    """The evaluate-expression task."""

    async def test_correct_result(self):
        gen = evaluate_expression.func(expression="3 + 2 * 3", expected=9)
        prompt = await gen.asend(None)
        assert "3 + 2 * 3" in prompt
        await add(2)
        await multiply(3)  # value = 6
        await add(3)  # value = 9
        reward = await gen.asend("Done")
        assert reward == 1.0

    async def test_wrong_result(self):
        gen = evaluate_expression.func(expression="5 + 5", expected=10)
        await gen.asend(None)
        await add(5)  # only added once, value = 5
        reward = await gen.asend("Done")
        assert reward == 0.0

    async def test_reset_between_tasks(self):
        # First task
        gen1 = evaluate_expression.func(expression="2 + 2", expected=4)
        await gen1.asend(None)
        await add(4)
        reward1 = await gen1.asend("Done")
        assert reward1 == 1.0
        assert _state["value"] == 4

        # Second task should reset
        gen2 = evaluate_expression.func(expression="3 + 3", expected=6)
        await gen2.asend(None)
        assert _state["value"] == 0  # reset on task start
        await add(6)
        reward2 = await gen2.asend("Done")
        assert reward2 == 1.0


class TestCalculatorTools:
    """The calculator tools."""

    def setup_method(self):
        _reset()

    async def test_add(self):
        result = await add(5)
        assert result == "Value: 5"
        assert _state["value"] == 5

    async def test_subtract(self):
        _state["value"] = 10
        result = await subtract(3)
        assert result == "Value: 7"
        assert _state["value"] == 7

    async def test_multiply(self):
        _state["value"] = 5
        result = await multiply(3)
        assert result == "Value: 15"
        assert _state["value"] == 15

    async def test_chained_operations(self):
        await add(5)
        await multiply(2)
        await subtract(3)
        assert _state["value"] == 7


class TestServedCapability:
    """The in-process MCP capability actually serves the calculator tools."""

    async def test_calculator_capability_serves_all_tools(self):
        from hud.capabilities.mcp import MCPClient

        await env.start()
        try:
            cap = env.capability("calculator")
            assert cap.protocol.startswith("mcp")
            client = await MCPClient.connect(cap)
            try:
                names = sorted(t.name for t in await client.list_tools())
                assert names == ["add", "get_value", "multiply", "subtract"]
            finally:
                await client.close()
        finally:
            await env.stop()
