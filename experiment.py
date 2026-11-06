# The big experiment: every test, at every level, several times.
# Each run becomes one row in results.csv, so strategies can be compared later without new API calls.
import csv
import os
import time

from dotenv import load_dotenv
from openai import RateLimitError

from car.agent import CarAssistant
from car.state import CarState
from level0_tests import TEST
from level1_noise import asr_style
from level2_audio import through_the_cabin

load_dotenv()

RUNS = 3
LEVELS = [0, 1, 2]


def same(actual, wanted):
    # "Munich airport." and "Munich Airport" mean the same place
    if isinstance(actual, str) and isinstance(wanted, str):
        return actual.lower().strip(" .") == wanted.lower().strip(" .")
    return actual == wanted


def check(state, expect):
    for key, wanted in expect.items():
        if not same(getattr(state, key), wanted):
            return False
    return True


def make_input(command, level):
    if level == 0:
        return command
    if level == 1:
        return asr_style(command)
    return through_the_cabin(command)


def ask_assistant(text, state):
    # The free NVIDIA account allows only so many calls per minute.
    # On "429 Too Many Requests" we wait and try again instead of crashing.
    for wait in [15, 30, 60, 120]:
        try:
            return assistant.handle(text, state)
        except RateLimitError:
            print(f"   rate limit, waiting {wait} s")
            time.sleep(wait)
    return assistant.handle(text, state)  # last try; if it still fails, stop


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
                ask_assistant(heard, state)
                seconds = round(time.time() - start, 2)

                passed = check(state, test["expect"])
                got = {key: getattr(state, key) for key in test["expect"]}
                writer.writerow([test["id"], level, run, int(passed), heard, got, seconds])
                f.flush()  # write each row right away, so a crash keeps what we have

        print(test["id"], "done")

print("Saved results.csv")
