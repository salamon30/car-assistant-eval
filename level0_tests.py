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

    # --- temperature: normal values, boundaries, refusals ---
    {"id": "t06", "command": "Set the temperature to 19 degrees", "expect": {"temperature_c": 19}},
    {"id": "t07", "command": "I'm cold, make it 24", "expect": {"temperature_c": 24}},
    {"id": "t08", "command": "Set the temperature to 16 degrees", "expect": {"temperature_c": 16}},
    {"id": "t09", "command": "Set the temperature to 28 degrees", "expect": {"temperature_c": 28}},
    {"id": "t10", "command": "Make it 35 degrees", "expect": {"temperature_c": 21.0}},
    {"id": "t11", "command": "Set the temperature to 10 degrees", "expect": {"temperature_c": 21.0}},
    {"id": "t12", "command": "Change the temperature to 23.5 degrees", "expect": {"temperature_c": 23.5}},
    {"id": "t13", "command": "Turn the heat down to 18", "expect": {"temperature_c": 18}},

    # --- volume: normal values, boundaries, clamping ---
    {"id": "t14", "command": "Set the volume to 3", "expect": {"volume": 3}},
    {"id": "t15", "command": "Mute the music", "expect": {"volume": 0}},
    {"id": "t16", "command": "Turn the volume all the way up", "expect": {"volume": 10}},
    {"id": "t17", "command": "Set the volume to 0", "expect": {"volume": 0}},
    {"id": "t18", "command": "Volume 4 please", "expect": {"volume": 4}},
    {"id": "t19", "command": "Set the volume to 12", "expect": {"volume": 10}},

    # --- navigation ---
    {"id": "t20", "command": "Navigate to Munich Central Station", "expect": {"destination": "Munich Central Station"}},
    {"id": "t21", "command": "Take me to Marienplatz", "expect": {"destination": "Marienplatz"}},
    {"id": "t22", "command": "Take me to Regensburg", "expect": {"destination": "Regensburg"}},
    {"id": "t23", "command": "Navigate to Nuremberg", "expect": {"destination": "Nuremberg"}},
    {"id": "t24", "command": "Take me to Frankfurt Airport", "expect": {"destination": "Frankfurt Airport"}},
    {"id": "t25", "command": "Navigate to Leopoldstrasse 12", "expect": {"destination": "Leopoldstrasse 12"}},

    # --- off-topic: nothing in the car may change ---
    {"id": "t26", "command": "What's the capital of France?",
     "expect": {"temperature_c": 21.0, "volume": 5, "destination": None}},
    {"id": "t27", "command": "Tell me a joke",
     "expect": {"temperature_c": 21.0, "volume": 5, "destination": None}},

    # --- two requests in one sentence ---
    {"id": "t28", "command": "Take me to Munich Airport and set the volume to 3",
     "expect": {"destination": "Munich Airport", "volume": 3}},
    {"id": "t29", "command": "Set the temperature to 20 and the volume to 6",
     "expect": {"temperature_c": 20, "volume": 6}},
    {"id": "t30", "command": "Make it 22 degrees and take me to Augsburg",
     "expect": {"temperature_c": 22, "destination": "Augsburg"}},
]
