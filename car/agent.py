"""The in-car assistant: an LLM that turns a spoken-style command into tool calls on CarState."""
import json
import os
import time
from dataclasses import dataclass, field

from openai import OpenAI, RateLimitError

from car.state import CarState, navigate_to, set_temperature, set_volume

MODEL = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
MAX_STEPS = 4  # model calls per command; stops a confused model from looping forever

SYSTEM_PROMPT = """You are the voice assistant of a car. Use the tools to carry out the driver's request.
Only call a tool when the driver asks for something the tool does. If a value is outside a tool's
range, still call the tool with exactly the value the driver said: the car limits or refuses it.
Never choose a different value or convert units yourself. If a tool returns an error,
tell the driver briefly. Answer in one short sentence, in the driver's language."""

# What the model sees: each tool's name, what it does and which arguments it takes (JSON Schema).
TOOLS = [
    {"type": "function", "function": {
        "name": "set_temperature",
        "description": "Set the cabin temperature in degrees Celsius. Allowed range 16-28.",
        "parameters": {"type": "object",
                       "properties": {"celsius": {"type": "number"}},
                       "required": ["celsius"]}}},
    {"type": "function", "function": {
        "name": "navigate_to",
        "description": "Start navigation to a place, e.g. an address, a city or 'nearest charging station'.",
        "parameters": {"type": "object",
                       "properties": {"place": {"type": "string"}},
                       "required": ["place"]}}},
    {"type": "function", "function": {
        "name": "set_volume",
        "description": "Set the media volume from 0 (mute) to 10 (max).",
        "parameters": {"type": "object",
                       "properties": {"level": {"type": "integer"}},
                       "required": ["level"]}}},
]

# What our code runs: tool name -> Python function.
FUNCTIONS = {
    "set_temperature": set_temperature,
    "navigate_to": navigate_to,
    "set_volume": set_volume,
}


@dataclass
class ToolCall:
    name: str
    arguments: dict
    result: str


@dataclass
class AgentResult:
    reply: str
    tool_calls: list[ToolCall] = field(default_factory=list)


class CarAssistant:
    def __init__(self, model: str = MODEL):
        self.client = OpenAI(base_url="https://integrate.api.nvidia.com/v1",
                             api_key=os.environ["NVIDIA_API_KEY"])
        self.model = model

    def _ask(self, messages):
        # The free NVIDIA tier allows only so many calls per minute: on 429, wait and retry.
        for wait in [15, 30, 60, 120]:
            try:
                return self.client.chat.completions.create(
                    model=self.model, messages=messages, tools=TOOLS,
                    temperature=0, max_tokens=4000)
            except RateLimitError:
                print(f"   rate limit, waiting {wait} s")
                time.sleep(wait)
        return self.client.chat.completions.create(
            model=self.model, messages=messages, tools=TOOLS, temperature=0, max_tokens=4000)

    def handle(self, command: str, state: CarState) -> AgentResult:
        messages = [{"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": command}]
        calls = []
        for _ in range(MAX_STEPS):
            response = self._ask(messages)
            message = response.choices[0].message
            if not message.tool_calls:  # no more tools wanted: this is the final answer
                return AgentResult(reply=(message.content or "").strip(), tool_calls=calls)

            messages.append(message)  # the model's request to call tools
            for tc in message.tool_calls:
                args = json.loads(tc.function.arguments)
                function = FUNCTIONS.get(tc.function.name)
                if function is None:
                    result = f"Error: unknown tool {tc.function.name}"
                else:
                    try:
                        result = function(state, **args)
                    except TypeError as e:  # wrong or missing arguments
                        result = f"Error: bad arguments ({e})"
                calls.append(ToolCall(tc.function.name, args, result))
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        return AgentResult(reply="Sorry, I could not finish that.", tool_calls=calls)


if __name__ == "__main__":
    assistant = CarAssistant()
    commands = [
        "Set the temperature to 22 degrees",
        "Make it 30 degrees in here",
        "Take me to Munich Airport and turn the music down to 3",
        "Mach bitte die Musik lauter, Stufe 8",
        "What's the capital of France?",
    ]
    for command in commands:
        car = CarState()
        result = assistant.handle(command, car)
        print(f"\n> {command}")
        for c in result.tool_calls:
            print(f"  tool: {c.name}({c.arguments}) -> {c.result}")
        print(f"  reply: {result.reply}")
        print(f"  state: {car}")
