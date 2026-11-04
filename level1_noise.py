# Level 1: make clean commands look like speech recognition output.

SOUND_ALIKE = {
    "to": "two",
    "munich": "munik",
    "7": "seven",
    "15": "fifteen",
    "22": "twenty two",
    "30": "thirty",
}


def asr_style(command):
    text = command.lower()
    words = text.split()
    new_words = []
    for word in words:
        if word in SOUND_ALIKE:
            new_words.append(SOUND_ALIKE[word])
        else:
            new_words.append(word)
    return " ".join(new_words)
