from dotenv import load_dotenv

from car.agent import CarAssistant
from car.checks import check
from car.state import CarState
from level0_tests import TEST

load_dotenv()


RUNS = 3

assistant = CarAssistant()
total_passed = 0

for test in TEST:
    passes = 0
    for run in range(RUNS):
        state = CarState()
        assistant.handle(test["command"], state)
        if check(state, test["expect"]):
            passes = passes + 1
    total_passed = total_passed + passes
    mark = "" if passes == RUNS else "   <-- fails"
    print(test["id"], passes, "/", RUNS, "->", test["command"], mark)

print("Total:", total_passed, "/", len(TEST) * RUNS)
