import json

from reach.apps.mqtt.message import Message
from reach.apps.mqtt.message.responses import GetGPSResponse


def serialize_message(message: Message) -> str:
    return json.dumps(message.to_dict())


def deserialize_message(message_json: str) -> Message:
    data = json.loads(message_json)
    # Hier kannst du anhand des "type"-Feldes entscheiden, welche Nachricht du erstellen möchtest
    if data["type"] == "get_gps":
        return GetGPSResponse(data)
    else:
        raise ValueError(f"Unbekannter Nachrichtentyp: {data['type']}")
