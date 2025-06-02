import json
from logging import Logger, getLogger
from typing import Any

from paho.mqtt.client import Client as MQTTClient

from reach.apps.flight_controller.utils import get_gps
from reach.apps.mqtt.message.responses import GetGPSResponse
from reach.config import COMMAND_TOPIC, RESPONSE_TOPIC, TOPIC
from reach.exceptions import NoMQTTConnectionException, NoVehicleConnectionException
from reach.thread_management import DroneState, message_queues


def on_connect(client: MQTTClient, userdata, flags, rc):
    logger: Logger = getLogger("mqtt_listener_daemon")
    if rc == 0:
        logger.info("✅ Connected with mqtt broker")
    else:
        logger.error(f"❌ Connection error: {rc}")
    client.subscribe(COMMAND_TOPIC)
    logger.info(f"📡 subscribed: {COMMAND_TOPIC}")


def on_message(client: MQTTClient, userdata, msg):
    logger: Logger = getLogger("mqtt_listener_daemon")
    logger.info(f"📥 received message on {msg.topic}: {msg.payload.decode()}")
    try:
        command: dict = json.loads(msg.payload.decode())
        handle_command(client, command)
    except Exception as e:
        logger.error(f"❌ Parsing error: {e}")


def send_response(client: MQTTClient, data):
    logger: Logger = getLogger("mqtt_listener_daemon")

    payload: str = json.dumps(data)
    client.publish(RESPONSE_TOPIC, payload)
    logger.info(f"📤 sent response: {payload}")


def handle_command(client: MQTTClient, command: dict):
    logger: Logger = getLogger("mqtt_listener_daemon")
    cmd_type = command.get("type")

    if cmd_type == "get_gps":

        # TODO: handle_command
        try:
            response: GetGPSResponse = get_gps()
        except NoVehicleConnectionException as e:
            res = {
                "type": "error",
                "message": "could not read gps data, flight controller might be offline",
            }
        else:
            res: dict[str, Any] = gps_data
            res["type"] = "get_gps"

        send_response(client, res)

    elif cmd_type == "ping":
        send_response(client, {"type": "ping", "status": "online"})

    else:
        logger.warning(f"⚠️ unknown command: {cmd_type}")
        send_response(
            client, {"type": "error", "message": f"unknown command: {cmd_type}"}
        )
