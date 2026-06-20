"""Sample tasks for the blank environment.

Run locally:   hud eval tasks.py claude
Sync remote:   hud sync tasks <taskset-name>

Calling a ``@env.template`` mints a runnable Task; we set a readable ``.slug``
on each. The vars are underscore-prefixed so ``hud eval`` discovers each task
once (via the ``tasks`` list), not twice.
"""

# env is re-exported so `hud eval tasks.py` can resolve the Environment from this file.
from env import count_letters, env, evaluate_expression  # noqa: F401

# -- count-letters: letter-counting tasks --------------------------------------
_count_r_strawberry = count_letters(word="strawberry", letter="r")
_count_r_strawberry.slug = "count-r-strawberry"

_count_s_mississippi = count_letters(word="mississippi", letter="s")
_count_s_mississippi.slug = "count-s-mississippi"

_count_e_bookkeeper = count_letters(word="bookkeeper", letter="e")
_count_e_bookkeeper.slug = "count-e-bookkeeper"

_count_a_banana = count_letters(word="banana", letter="a")
_count_a_banana.slug = "count-a-banana"

# -- evaluate-expression: math tasks -------------------------------------------
_eval_order_of_ops = evaluate_expression(expression="3 + 2 * 3", expected=9)
_eval_order_of_ops.slug = "eval-order-of-ops"

_eval_parens = evaluate_expression(expression="(2 + 3) * 4", expected=20)
_eval_parens.slug = "eval-parens"

_eval_mixed = evaluate_expression(expression="10 - 2 * 3 + 1", expected=5)
_eval_mixed.slug = "eval-mixed"

tasks = [
    _count_r_strawberry,
    _count_s_mississippi,
    _count_e_bookkeeper,
    _count_a_banana,
    _eval_order_of_ops,
    _eval_parens,
    _eval_mixed,
]
