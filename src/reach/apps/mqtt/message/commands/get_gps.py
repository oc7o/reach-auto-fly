from typing import Any, ClassVar, Optional

from reach.apps.mqtt.message import Message
from reach.apps.mqtt.message.responses import GetGPSResponse
from reach.thread_management import drone_state


class GetGPSCommand(Message):
    message_type: ClassVar[str] = "command"
    command: ClassVar[str] = "get_gps"

    def __init__(self, data: Optional[dict[str, Any]]) -> None:
        super().__init__(data)
        if data is not None:
            self.from_dict(data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_type": self.message_type,
            "command": self.command,
            "uuid": self.uuid,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        if "uuid" in data.values():
            self.uuid = data["uuid"]

    @classmethod
    def handle_command(cls) -> GetGPSResponse:
        assert drone_state.gps_location is not None
        return GetGPSResponse(
            {
                "lat": drone_state.gps_location["lat"],
                "lon": drone_state.gps_location["lon"],
                "alt": drone_state.gps_location["alt"],  # relative
                "alt_abs": drone_state.gps_location["alt_abs"],
                "statelites_visible": drone_state.gps_location["statelites_visible"],
            }
        )
