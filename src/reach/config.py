import os

from dotenv import load_dotenv

load_dotenv()

# PERSON_RECOGNITION_ACCEPTANCE: float = float(
#     os.environ.get("PERSON_RECOGNITION_ACCEPTANCE", 0.2)
# )


# RECOGNITION & AI STUFF
PERSON_RECOGNITION_ACCEPTANCE: float = 0.3
MAX_PANTS_COLOR_DELTA = 15
MAX_TSHIRT_COLOR_DELTA = 15
MIN_PERSON_COMPARISON_MATCH_LEVEL_1 = 0.85
MIN_PERSON_COMPARISON_MATCH_LEVEL_2 = 0.75
MAX_PERSONS_TRACKED = 4
DELETE_PERSON_AFTER_N_SECONDS = 5
MAX_PERSON_DATA_LIST_ENTRIES = 4


# SIMULATION
SIMULATION_FRAME_SKIP = 5  # Default 1

# MQTT
BROKER_IP = os.environ.get(
    "REACH_MQTT_BROKER", "127.0.0.1"
)  # IP of the MQTT broker (e.g. Raspberry Pi / Mosquitto)
TOPIC = "reach/drone"  # will deprecate

COMMAND_TOPIC = "reach/command"
RESPONSE_TOPIC = "reach/response"

GPS_TOPIC = "reach/drone/gps"
# CLIENT_ID = "reach_drone"

# FLIGHT CONTROL
MAXIMUM_WAIT_COUNT = 5
