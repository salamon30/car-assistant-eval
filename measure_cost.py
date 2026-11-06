import time

from dotenv import load_dotenv

from car.agent import CarAssistant
from car.state import CarState
from level1_noise import asr_style
from level2_audio import through_the_cabin

load_dotenv()
assistant = CarAssistant()
command = "Set the temperature to 22 degrees"

start = time.time()
assistant.handle(command, CarState())
print("Level 0:", round(time.time() - start, 1), "seconds")

start = time.time()
assistant.handle(asr_style(command), CarState())
print("Level 1:", round(time.time() - start, 1), "seconds")

start = time.time()
assistant.handle(through_the_cabin(command), CarState())
print("Level 2:", round(time.time() - start, 1), "seconds")