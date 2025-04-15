from reach.config import TOPIC
from reach.thread_management import drone_state, loggers, message_queues


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"MESSAGE RECEIVED: {message}")
    flight_controller_commands = ["takeUp", "land", "holdPosition"]

    if message == "emergency":
        drone_state.emergency = True

    elif message in flight_controller_commands:
        message_queues["flight_controller_daemon"].put(message)

    elif message == "getDronePosition":

        # print("Global Location: %s" % drone_state.vehicle.location.global_frame)
        # print(
        #     "Global Location (relative altitude): %s"
        #     % drone_state.vehicle.location.global_relative_frame
        # )
        # print("Local Location: %s" % drone_state.vehicle.location.local_frame)  # NED

        global_location = drone_state.vehicle.location.global_frame
        global_location_ra = drone_state.vehicle.location.global_relative_frame

        latitude = global_location.lat
        longitude = global_location.lon
        absolute_altitude = global_location.alt
        relative_altitude = global_location_ra.alt
        response = (
            str(latitude)
            + "|"
            + str(longitude)
            + "|"
            + str(absolute_altitude)
            + "|"
            + str(relative_altitude)
        )

        client.publish(TOPIC, response)


def send_message(topic, message):
    if drone_state.mqtt_client is None:
        loggers["mqtt_listener_daemon"].warning("Not connected to mqtt server")
    else:
        drone_state.mqtt_client.publish(topic, message)
