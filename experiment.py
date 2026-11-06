# The big experiment: every test, at every level, several times.
# Each run becomes one row in results.csv, so strategies can be compared later without new API calls.
import csv
import os
import time

from dotenv import load_dotenv

from car.agent import CarAssistant
from car.checks import check
from car.state import CarState
from level0_tests import TEST
from level1_noise import asr_style
from level2_audio import through_the_cabin

load_dotenv()

RUNS = 3
LEVELS = [0, 1, 2]


def make_input(command, level):
    if level == 0:
        return command
    if level == 1:
        return asr_style(command)
    return through_the_cabin(command)


def already_done():
    # Runs that are already in results.csv, so a restart continues where it stopped
    if not os.path.exists("results.csv"):
        return set()
    with open("results.csv") as f:
        return {(r["test_id"], int(r["level"]), int(r["run"])) for r in csv.DictReader(f)}


assistant = CarAssistant()
done = already_done()

with open("results.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not done:
        writer.writerow(["test_id", "level", "run", "passed", "heard", "got", "seconds"])

    for test in TEST:
        for level in LEVELS:
            for run in range(RUNS):
                if (test["id"], level, run) in done:
                    continue
                start = time.time()
                heard = make_input(test["command"], level)
                state = CarState()
                assistant.handle(heard, state)
                seconds = round(time.time() - start, 2)

                passed = check(state, test["expect"])
                got = {key: getattr(state, key) for key in test["expect"]}
                writer.writerow([test["id"], level, run, int(passed), heard, got, seconds])
                f.flush()  # write each row right away, so a crash keeps what we have

        print(test["id"], "done")

print("Saved results.csv")
