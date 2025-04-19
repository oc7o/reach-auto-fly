import json
import logging

from reach.apps.flight_controller.utils import get_gps
from reach.config import COMMAND_TOPIC, RESPONSE_TOPIC, TOPIC
from reach.thread_management import drone_state, message_queues


def handle_command(client, command):
    cmd_type = command.get("type")

    if cmd_type == "get_gps":
        gps_data = get_gps()
        if gps_data is None:
            res = {
                "type": "error",
                "message": "could not read gps data, flight controller might be offline",
            }
        else:
            res = gps_data
            res["type"] = "get_gps"

        send_response(client, res)

    elif cmd_type == "ping":
        send_response(client, {"type": "ping", "status": "online"})

    else:
        logging.getLogger("mqtt_listener_daemon").warning(
            f"⚠️ unknown command: {cmd_type}"
        )
        send_response(
            client, {"type": "error", "message": f"unknown command: {cmd_type}"}
        )


def send_response(client, data):
    payload = json.dumps(data)
    client.publish(RESPONSE_TOPIC, payload)
    logging.getLogger("mqtt_listener_daemon").info(f"📤 sent response: {payload}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.getLogger("mqtt_listener_daemon").info("✅ Connected with mqtt broker")
    else:
        logging.getLogger("mqtt_listener_daemon").error(f"❌ Connection error: {rc}")
    client.subscribe(COMMAND_TOPIC)
    logging.getLogger("mqtt_listener_daemon").info(f"📡 subscribed: {COMMAND_TOPIC}")


def on_message(client, userdata, msg):
    logging.getLogger("mqtt_listener_daemon").info(
        f"📥 received message on {msg.topic}: {msg.payload.decode()}"
    )
    try:
        command = json.loads(msg.payload.decode())
        handle_command(client, command)
    except Exception as e:
        logging.getLogger("mqtt_listener_daemon").error(f"❌ Parsing error: {e}")

    # pass

    # message = msg.payload.decode()
    # print(f"MESSAGE RECEIVED: {message}")
    # flight_controller_commands = ["takeUp", "land", "holdPosition"]

    # if message == "emergency":
    #     drone_state.emergency = True

    # elif message in flight_controller_commands:
    #     message_queues["flight_controller_daemon"].put(message)

    # elif message == "getDronePosition":

    #     # print("Global Location: %s" % drone_state.vehicle.location.global_frame)
    #     # print(
    #     #     "Global Location (relative altitude): %s"
    #     #     % drone_state.vehicle.location.global_relative_frame
    #     # )
    #     # print("Local Location: %s" % drone_state.vehicle.location.local_frame)  # NED

    #     global_location = drone_state.vehicle.location.global_frame
    #     global_location_ra = drone_state.vehicle.location.global_relative_frame

    #     latitude = global_location.lat
    #     longitude = global_location.lon
    #     absolute_altitude = global_location.alt
    #     relative_altitude = global_location_ra.alt
    #     response = (
    #         str(latitude)
    #         + "|"
    #         + str(longitude)
    #         + "|"
    #         + str(absolute_altitude)
    #         + "|"
    #         + str(relative_altitude)
    #     )

    #     client.publish(TOPIC, response)


def send_message(topic, message):
    if drone_state.mqtt_client is None:
        logging.getLogger("mqtt_listener_daemon").warning(
            "Not connected to mqtt server"
        )
    else:
        drone_state.mqtt_client.publish(topic, message)
