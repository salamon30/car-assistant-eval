import random

from simulate import REAL_BUGS, STRATEGIES, TESTS, outcomes, simulate

COST = {0: 1, 1: 1, 2: 3}


def test_no_budget_finds_nothing():
    for strategy in STRATEGIES:
        assert simulate(strategy, 0, COST, random.Random(0)) == 0


def test_level0_only_finds_just_the_bugs_visible_in_clean_text():
    visible = {t for t in REAL_BUGS if 0 in outcomes[(t, 0)]}
    found = simulate("B: only level 0", 1000, COST, random.Random(0))
    assert found == len(visible)


def test_large_budget_finds_every_real_bug():
    found = simulate("A: only level 2", 5000, COST, random.Random(0))
    assert found == len(REAL_BUGS)


def test_found_never_exceeds_real_bugs():
    for strategy in STRATEGIES:
        for budget in (30, 90, 270):
            assert simulate(strategy, budget, COST, random.Random(1)) <= len(REAL_BUGS) <= len(TESTS)
