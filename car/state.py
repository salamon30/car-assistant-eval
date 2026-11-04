"""The mock car: its state and the tools an assistant can call to change it."""
from dataclasses import dataclass


@dataclass(slots=True)  # slots: a misspelled field name raises an error instead of being silently added
class CarState:
    temperature_c: float = 21.0
    fan_level: int = 2          # 0-5
    destination: str | None = None
    media_playing: str | None = None
    volume: int = 5             # 0-10


def set_temperature(state: CarState, celsius: float) -> str:
    """Set cabin temperature. Out-of-range requests are refused, state unchanged."""
    if celsius < 16 or celsius > 28:
        return f"Error: {celsius} °C is outside the allowed range 16-28 °C"
    state.temperature_c = celsius
    return f"Temperature set to {celsius} °C"


def navigate_to(state: CarState, place: str) -> str:
    """Start navigation to a place."""
    state.destination = place
    return f"Navigating to {place}"


def set_volume(state: CarState, level: int) -> str:
    """Set media volume, clamped to 0-10."""
    level = max(0, min(10, level))
    state.volume = level
    return f"Volume set to {level}"


if __name__ == "__main__":
    car = CarState()
    print("Start:", car)
    print(set_temperature(car, 30))
    print(set_temperature(car, 22))
    print(navigate_to(car, "Munich Airport"))
    print(set_volume(car, 15))
    print("End:  ", car)
