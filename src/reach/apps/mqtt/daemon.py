import paho.mqtt.client as mqtt

from reach.apps.mqtt.mqtt import on_connect, on_message
from reach.config import BROKER_IP


def mqtt_listener_daemon():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_IP, 1883, 60)
    client.loop_forever()  # Lässt den Client dauerhaft laufen
