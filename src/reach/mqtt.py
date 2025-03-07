from reach.config import TOPIC
from reach.mqtt import drone_state
from reach.thread_management import drone_state, message_queues


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"MESSAGE RECEIVED: {message}")
    flight_controller_commands = ["takeUp", "land"]

    if message == "emergency":
        drone_state.emergency = True

    elif message in flight_controller_commands:
        message_queues["flight_controller_daemon"].put(message)

    elif message == "holdPosition":
        pass

    elif message == "getDronePosition":
        latitude = drone_state.vehicle.location.global_relative_frame.lat
        longitude = drone_state.vehicle.location.global_relative_frame.lon
        altitude = None
