"""Sample tasks for the blank environment.

Each task is created via scenario.task() and can be run locally:

    python local_test.py --list
    python local_test.py --task count_r_strawberry
    python local_test.py --task eval_order_of_ops --model gpt-4o
"""

from env import count_letters, evaluate_expression

# -- count-letters: letter counting challenges ---------------------------------

count_r_strawberry = count_letters.task(word="strawberry", letter="r")
count_r_strawberry.slug = "count-r-strawberry"

count_s_mississippi = count_letters.task(word="mississippi", letter="s")
count_s_mississippi.slug = "count-s-mississippi"

count_e_bookkeeper = count_letters.task(word="bookkeeper", letter="e")
count_e_bookkeeper.slug = "count-e-bookkeeper"

count_a_banana = count_letters.task(word="banana", letter="a")
count_a_banana.slug = "count-a-banana"

# -- evaluate-expression: math expression challenges ---------------------------

eval_order_of_ops = evaluate_expression.task(expression="3 + 2 * 3", expected=9)
eval_order_of_ops.slug = "eval-order-of-ops"

eval_parens = evaluate_expression.task(expression="(2 + 3) * 4", expected=20)
eval_parens.slug = "eval-parens"

eval_mixed = evaluate_expression.task(expression="10 - 2 * 3 + 1", expected=5)
eval_mixed.slug = "eval-mixed"

# -- registry for discovery ----------------------------------------------------

ALL_TASKS = {
    "count_r_strawberry": count_r_strawberry,
    "count_s_mississippi": count_s_mississippi,
    "count_e_bookkeeper": count_e_bookkeeper,
    "count_a_banana": count_a_banana,
    "eval_order_of_ops": eval_order_of_ops,
    "eval_parens": eval_parens,
    "eval_mixed": eval_mixed,
}
