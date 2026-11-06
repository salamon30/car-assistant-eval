"""Did the car end up where the test expected? Shared by every runner, so all levels judge the same way."""


def same(actual, wanted):
    # "Munich airport." and "Munich Airport" mean the same place
    if isinstance(actual, str) and isinstance(wanted, str):
        return actual.lower().strip(" .") == wanted.lower().strip(" .")
    return actual == wanted


def check(state, expect):
    """True if every expected field of the car state matches."""
    for key, wanted in expect.items():
        if not same(getattr(state, key), wanted):
            return False
    return True
