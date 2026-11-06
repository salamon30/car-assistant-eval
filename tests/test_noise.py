from level1_noise import asr_style


def test_numbers_become_words_and_to_becomes_two():
    assert asr_style("Set the temperature to 22 degrees") == "set the temperature two twenty two degrees"


def test_unknown_words_are_kept_lowercased():
    assert asr_style("Tell me a Joke") == "tell me a joke"
