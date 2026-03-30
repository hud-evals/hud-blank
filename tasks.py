"""Sample tasks for the blank environment.

Each task is created via scenario.task() and can be run locally or remotely:

    python local_test.py --list
    python local_test.py --task count_to_3
    python local_test.py --task reach_efficient_100 --model gpt-4o
"""

from env import (
    compute_expression,
    count_to,
)

# -- count-to: partial credit (simple float reward) ---------------------------

count_to_3 = count_to.task(target=3)
count_to_3.slug = "count-to-3"

count_to_10 = count_to.task(target=10)
count_to_10.slug = "count-to-10"

# -- compute-expression: agent reasoning / planning ---------------------------

compute_add_multiply = compute_expression.task(expression="3 * 4 + 5", expected=17)
compute_add_multiply.slug = "compute-add-mul"

compute_mixed = compute_expression.task(expression="(2 + 3) * 7 - 5", expected=30)
compute_mixed.slug = "compute-mixed"

# -- registry for discovery ----------------------------------------------------

ALL_TASKS = {
    "count_to_3": count_to_3,
    "count_to_10": count_to_10,
    "compute_add_multiply": compute_add_multiply,
    "compute_mixed": compute_mixed,
}
