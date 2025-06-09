from logging import Logger, getLogger

from paho.mqtt.client import Client as MQTTClient

from reach.apps.mqtt.mqtt import on_connect, on_message
from reach.config import BROKER_IP
from reach.thread_management import DroneState


def mqtt_listener_daemon() -> None:
    logger: Logger = getLogger("mqtt_listener_daemon")

    client: MQTTClient = MQTTClient()
    client.on_connect = on_connect
    client.on_message = on_message

    DroneState.mqtt_client = client

    try:
        client.connect(BROKER_IP, 1883, 60)
    except OSError:
        logger.warning("Unable to connect to MQTT-Server.")
    client.loop_forever()  # Lässt den Client dauerhaft laufen
