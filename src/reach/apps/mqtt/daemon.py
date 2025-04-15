import paho.mqtt.client as mqtt

from reach.apps.mqtt.mqtt import on_connect, on_message
from reach.config import BROKER_IP
from reach.thread_management import drone_state, loggers


def mqtt_listener_daemon():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    drone_state.mqtt_client = client

    try:
        client.connect(BROKER_IP, 1883, 60)
    except OSError:
        loggers["mqtt_listener_daemon"].warning("Unable to connect to MQTT-Server.")
    client.loop_forever()  # Lässt den Client dauerhaft laufen
