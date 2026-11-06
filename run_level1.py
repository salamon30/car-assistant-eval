from dotenv import load_dotenv

from car.agent import CarAssistant
from car.checks import check
from car.state import CarState
from level0_tests import TEST
from level1_noise import asr_style

load_dotenv()


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
