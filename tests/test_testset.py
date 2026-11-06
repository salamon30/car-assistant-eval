from dataclasses import fields

from car.state import CarState
from level0_tests import TEST

CAR_FIELDS = {f.name for f in fields(CarState)}


def test_thirty_tests_with_unique_ids():
    ids = [t["id"] for t in TEST]
    assert len(ids) == 30
    assert len(set(ids)) == 30


def test_every_expectation_names_a_real_car_field():
    for test in TEST:
        assert test["command"].strip()
        assert set(test["expect"]) <= CAR_FIELDS, test["id"]
