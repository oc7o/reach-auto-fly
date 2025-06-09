import json
from logging import Logger, getLogger
from typing import Any

from paho.mqtt.client import Client as MQTTClient

from reach.apps.mqtt.message.commands import (
    GotoLocationCommand,
    HoldPositionCommand,
    LandCommand,
    TakeoffCommand,
)
from reach.config import COMMAND_TOPIC, RESPONSE_TOPIC
from src.reach.apps.mqtt.message.commands.relative_move import (
    RelativeMoveCommand,
)
from src.reach.thread_management import DroneState


def on_connect(client: MQTTClient, userdata, flags, rc) -> None:
    logger: Logger = getLogger("mqtt_listener_daemon")
    if rc == 0:
        logger.info("✅ Connected with mqtt broker")
    else:
        logger.error(f"❌ Connection error: {rc}")
    client.subscribe(COMMAND_TOPIC)
    logger.info(f"📡 subscribed: {COMMAND_TOPIC}")


def on_message(client: MQTTClient, userdata, msg) -> None:
    logger: Logger = getLogger("mqtt_listener_daemon")
    logger.info(f"📥 received message on {msg.topic}: {msg.payload.decode()}")
    try:
        command: dict = json.loads(msg.payload.decode())
        handle_command(client, command)
    except Exception as e:
        logger.error(f"❌ Parsing error: {e}")


def send_response(data: dict[str, Any]) -> None:
    assert DroneState.mqtt_client is not None
    client: MQTTClient = DroneState.mqtt_client

    logger: Logger = getLogger("mqtt_listener_daemon")

    payload: str = json.dumps(data)
    client.publish(RESPONSE_TOPIC, payload)
    logger.info(f"📤 sent response: {payload}")


def handle_command(client: MQTTClient, payload: dict) -> None:
    logger: Logger = getLogger("mqtt_listener_daemon")
    message_type = payload.get("message_type")
    command = payload.get("command")

    if message_type == "command":
        if command == GotoLocationCommand.command:
            GotoLocationCommand.handle_command(payload)

        elif command == TakeoffCommand.command:
            TakeoffCommand.handle_command(payload)

        elif command == LandCommand.command:
            LandCommand.handle_command(payload)

        elif command == HoldPositionCommand.command:
            HoldPositionCommand.handle_command(payload)

        elif command == RelativeMoveCommand.command:
            RelativeMoveCommand.handle_command(payload)

            # elif cmd_type == "get_gps":

            #     # TODO: handle_command
            #     try:
            #         response: GetGPSResponse = get_gps()
            #     except NoVehicleConnectionException as e:
            #         res = {
            #             "type": "error",
            #             "message": "could not read gps data, flight controller might be offline",
            #         }
            #     else:
            #         res: dict[str, Any] = gps_data
            #         res["type"] = "get_gps"
            #
            # send_response(client, res)

        elif command == "ping":
            send_response({"type": "ping", "status": "online"})

        else:
            logger.warning(f"⚠️ unknown command: {command}")
            send_response(
                {"type": "error", "message": f"unknown command: {command}"},
            )
