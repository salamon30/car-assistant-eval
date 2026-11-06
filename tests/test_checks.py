from car.checks import check, same
from car.state import CarState


def test_same_ignores_case_and_trailing_period():
    assert same("Munich airport.", "Munich Airport")


def test_same_compares_numbers_exactly():
    assert same(22, 22.0)
    assert not same(22.2, 22)


def test_check_needs_every_field_to_match():
    car = CarState(temperature_c=22, destination="Augsburg")
    assert check(car, {"temperature_c": 22, "destination": "augsburg"})
    assert not check(car, {"temperature_c": 22, "destination": "Oxford"})


def test_check_handles_no_destination():
    assert check(CarState(), {"destination": None})
