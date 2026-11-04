# Level 0: clean text commands and what the car should look like afterwards.
TEST = [
    {
        "id": "t01",
        "command": "Set the temperature to 22 degrees",
        "expect": {"temperature_c": 22},
    },
    {
        "id": "t02",
        "command": "Make it 30 degrees in here",
        "expect": {"temperature_c": 21.0}, # 30 is not allowed, so nothing changes

    },

    {
        "id": "t03",
        "command": "Take me to Munich Airport",
        "expect": {"destination": "Munich Airport"},
    },

    {
        "id": "t04",
        "command": "Set the volume to 7",
        "expect": {"volume": 7},
    },

    {
        "id": "t05",
        "command": "Make the sound 15",
        "expect": {"volume": 10},
    },

    ]

