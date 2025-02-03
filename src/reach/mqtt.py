from reach.config import TOPIC
from reach.thread_management import message_queues


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"MESSAGE RECEIVED: {message}")
    flight_controller_commands = ["takeUp", "land"]

    if message in flight_controller_commands:
        message_queues["flight_controller_daemon"].put(message)
