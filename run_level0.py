from dotenv import load_dotenv

from car.agent import CarAssistant
from car.state import CarState
from level0_tests import TEST

load_dotenv()


def check(state, expect):
    for key, wanted in expect.items():
        actual = getattr(state, key)
        if actual != wanted:
            return False
    return True


assistant = CarAssistant()
passed = 0

for test in TEST:
    state = CarState()
    result = assistant.handle(test["command"], state)
    ok = check(state, test["expect"])

    if ok:
        passed = passed + 1
        print(test["id"], "PASS", "->", test["command"])
    else:
        print(test["id"], "FAIL", "->", test["command"])
        print("   car state:", state)

print(passed, "/", len(TEST), "passed")
