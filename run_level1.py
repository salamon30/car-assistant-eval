from dotenv import load_dotenv

from car.agent import CarAssistant
from car.state import CarState
from level0_tests import TEST
from level1_noise import asr_style

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
    noisy = asr_style(test["command"])
    passes = 0
    values = []  # what the car ended up with in each run

    for run in range(RUNS):
        state = CarState()
        assistant.handle(noisy, state)
        if check(state, test["expect"]):
            passes = passes + 1
        for key in test["expect"]:
            values.append(getattr(state, key))

    total_passed = total_passed + passes
    print(test["id"], passes, "/", RUNS, "->", noisy)
    print("   expected:", test["expect"], " got:", values)

print("Total:", total_passed, "/", len(TEST) * RUNS)
