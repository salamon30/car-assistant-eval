"""The tool-calling loop with a fake LLM client: no API key, no network."""
import json
from types import SimpleNamespace as NS

from car.agent import MAX_STEPS, CarAssistant
from car.state import CarState


def tool_call(name, args, call_id="c1"):
    return NS(id=call_id, function=NS(name=name, arguments=json.dumps(args)))


class FakeClient:
    """Returns the given messages one by one, like a scripted model."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        reply = self.replies.pop(0) if self.replies else self.last
        self.last = reply
        return NS(choices=[NS(message=reply)])


def assistant_with(replies):
    assistant = CarAssistant.__new__(CarAssistant)  # skip __init__, which needs an API key
    assistant.client = FakeClient(replies)
    assistant.model = "fake"
    return assistant


def test_tool_call_changes_the_car_and_is_recorded():
    replies = [NS(tool_calls=[tool_call("set_temperature", {"celsius": 22})], content=None),
               NS(tool_calls=None, content="Temperature set to 22 °C.")]
    car = CarState()
    result = assistant_with(replies).handle("Set the temperature to 22 degrees", car)
    assert car.temperature_c == 22
    assert result.reply == "Temperature set to 22 °C."
    assert [c.name for c in result.tool_calls] == ["set_temperature"]


def test_unknown_tool_becomes_an_error_not_a_crash():
    replies = [NS(tool_calls=[tool_call("open_sunroof", {})], content=None),
               NS(tool_calls=None, content="Sorry.")]
    result = assistant_with(replies).handle("Open the sunroof", CarState())
    assert result.tool_calls[0].result.startswith("Error: unknown tool")


def test_bad_arguments_become_an_error_not_a_crash():
    replies = [NS(tool_calls=[tool_call("set_volume", {"loudness": 3})], content=None),
               NS(tool_calls=None, content="Sorry.")]
    result = assistant_with(replies).handle("Volume 3", CarState())
    assert result.tool_calls[0].result.startswith("Error: bad arguments")


def test_loop_stops_after_max_steps():
    looping = NS(tool_calls=[tool_call("set_volume", {"level": 3})], content=None)
    result = assistant_with([looping]).handle("Volume 3", CarState())
    assert len(result.tool_calls) == MAX_STEPS
    assert result.reply == "Sorry, I could not finish that."
