# Budget simulation: which testing strategy finds the most bugs for the same cost?
# Uses only results.csv, so it is free and instant (no API calls).
import csv
import random
from collections import defaultdict

REPEATS = 300  # each strategy is simulated many times with random luck, then averaged

# Read the experiment: for every (test, level) the recorded pass/fail outcomes
outcomes = defaultdict(list)
with open("results.csv") as f:
    for row in csv.DictReader(f):
        outcomes[(row["test_id"], int(row["level"]))].append(int(row["passed"]))

TESTS = sorted({test_id for test_id, level in outcomes})

# A "real bug" = a test that failed at least once at level 2, our most realistic level.
REAL_BUGS = {t for t in TESTS if 0 in outcomes[(t, 2)]}


def simulate(strategy, budget, cost, rng):
    found = set()
    spent = 0

    def run(test, level):
        """Pay for one run and look up a recorded outcome. Returns True/False, or None if no money left."""
        nonlocal spent
        if spent + cost[level] > budget:
            return None
        spent += cost[level]
        passed = rng.choice(outcomes[(test, level)])
        if not passed and test in REAL_BUGS:
            found.add(test)
        return passed

    order = TESTS[:]
    rng.shuffle(order)

    if strategy == "A: only level 2":
        queue = order
    elif strategy == "B: only level 0":
        while spent + cost[0] <= budget:
            for test in order:
                run(test, 0)
        return len(found)
    elif strategy == "C: level 0 first, then level 2":
        for test in order:
            run(test, 0)
        queue = [t for t in order if t not in found]
    elif strategy == "D: level 1 first, suspects go to level 2 first":
        suspects = [t for t in order if run(t, 1) is False]
        queue = suspects + [t for t in order if t not in suspects]

    while spent + cost[2] <= budget:
        for test in queue:
            run(test, 2)
    return len(found)


STRATEGIES = ["A: only level 2", "B: only level 0",
              "C: level 0 first, then level 2", "D: level 1 first, suspects go to level 2 first"]

if __name__ == "__main__":
    print("Real bugs to find:", len(REAL_BUGS), "of", len(TESTS), "tests\n")

    scenarios = {
        "Measured cost (level 2 = 3x)": ({0: 1, 1: 1, 2: 3}, [30, 60, 90, 180]),
        "Real car cost (level 2 = 20x)": ({0: 1, 1: 1, 2: 20}, [100, 200, 400, 800]),
    }
    for name, (cost, budgets) in scenarios.items():
        print(name)
        print("   budget:", budgets)
        for strategy in STRATEGIES:
            averages = []
            for budget in budgets:
                rng = random.Random(0)
                total = sum(simulate(strategy, budget, cost, rng) for _ in range(REPEATS))
                averages.append(round(total / REPEATS, 1))
            print("  ", averages, strategy)
        print()
