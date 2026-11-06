from dotenv import load_dotenv

from car.agent import CarAssistant
from car.state import CarState
from level0_tests import TEST
from level2_audio import through_the_cabin

load_dotenv()


def check(state, expect):
    for key, wanted in expect.items():
        actual = getattr(state, key)
        if actual != wanted:
            return False
    return True


RUNS = 3

assistant = CarAssistant()
total_passed = 0

for test in TEST:
    passes = 0
    values = []
    heard_list = []

    for run in range(RUNS):
        noisy = through_the_cabin(test["command"])
        heard_list.append(noisy)

        state = CarState()
        assistant.handle(noisy, state)
        if check(state, test["expect"]):
            passes = passes + 1
        for key in test["expect"]:
            values.append(getattr(state, key))

    total_passed = total_passed + passes
    print(test["id"], passes, "/", RUNS, "->", test["command"])
    print("   heard:", heard_list)
    print("   expected:", test["expect"], " got:", values)

print("Total:", total_passed, "/", len(TEST) * RUNS)
