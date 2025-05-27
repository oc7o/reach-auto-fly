from typing import Any, ClassVar, Optional

from reach.apps.mqtt.message import Message


class GetGPSResponse(Message):
    message_type: ClassVar[str] = "response"
    command: ClassVar[str] = "get_gps"

    lat: float
    lon: float
    alt: float
    alt_abs: float
    satelites_visible: int

    def __init__(self, data: Optional[dict[str, Any]]) -> None:
        super().__init__(data)
        if data is not None:
            self.from_dict(data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_type": self.message_type,
            "command": self.command,
            "uuid": self.uuid,
            "lat": self.lat,
            "lon": self.lon,
            "alt": self.alt,
            "alt_abs": self.alt_abs,
            "satelites_visible": self.satelites_visible,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        self.lat = data["lat"]
        self.lon = data["lon"]
        self.alt = data["alt"]
        self.alt_abs = data["alt_abs"]
        self.satelites_visible = data["satelites_visible"]
        if "uuid" in data.values():
            self.uuid = data["uuid"]
