from car.state import CarState, navigate_to, set_temperature, set_volume


def test_temperature_inside_range_is_set():
    car = CarState()
    set_temperature(car, 22)
    assert car.temperature_c == 22


def test_temperature_boundaries_are_allowed():
    car = CarState()
    set_temperature(car, 16)
    assert car.temperature_c == 16
    set_temperature(car, 28)
    assert car.temperature_c == 28


def test_temperature_outside_range_is_refused_and_state_unchanged():
    car = CarState()
    message = set_temperature(car, 30)
    assert message.startswith("Error")
    assert car.temperature_c == 21.0


def test_volume_is_clamped_to_0_10():
    car = CarState()
    set_volume(car, 15)
    assert car.volume == 10
    set_volume(car, -3)
    assert car.volume == 0


def test_navigate_sets_destination():
    car = CarState()
    navigate_to(car, "Munich Airport")
    assert car.destination == "Munich Airport"
