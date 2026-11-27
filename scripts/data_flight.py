import json
import os
import time
from typing import Any

from paho.mqtt.client import Client as MQTTClient

client: MQTTClient = MQTTClient()


COMMAND_TOPIC = "reach/command"

client.connect(os.environ.get("REACH_MQTT_BROKER", "127.0.0.1"), 1883, 60)


def exec_command(command: dict[str, Any], client: MQTTClient) -> None:
    """
    Execute a command by publishing it to the MQTT broker.

    :param command: The command to execute, as a dictionary.
    :param client: The MQTT client to use for publishing.
    """
    topic = COMMAND_TOPIC
    payload = json.dumps(command)
    client.publish(topic, payload)
    # print(f"Command published to {topic}: {payload}")


exec_command(
    {
        "type": "command",
        "command": "takeoff",
    },
    client,
)
time.sleep(10)
exec_command(
    {
        "type": "command",
        "command": "hold_position",
    },
    client,
)
time.sleep(10)
exec_command(
    {
        "type": "command",
        "command": "relative_move",
        "x": 1.0,  # forward movement in meters
    },
    client,
)
time.sleep(10)
exec_command(
    {
        "type": "command",
        "command": "hold_position",
    },
    client,
)
time.sleep(10)
exec_command(
    {
        "type": "command",
        "command": "land",
    },
    client,
)
