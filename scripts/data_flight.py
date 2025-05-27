import json

from paho.mqtt.client import Client as MQTTClient

client: MQTTClient = MQTTClient()


COMMAND_TOPIC = "reach/command"

client.connect("127.0.0.1", 1883, 60)

data = {}
payload: str = json.dumps(data)
client.publish(COMMAND_TOPIC, payload)
