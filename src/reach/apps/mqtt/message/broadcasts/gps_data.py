from typing import Any, ClassVar, Optional

from reach.apps.flight_controller.gps_data import GPSData
from reach.apps.mqtt.message import Message


class GPSDataBroadcast(Message):
    message_type: ClassVar[str] = "broadcast"
    command: ClassVar[str] = "gps_data"

    gps_data: GPSData

    def __init__(self, gps_data: Optional[GPSData]) -> None:
        if gps_data is not None:
            self.gps_data = gps_data

    def to_dict(self) -> dict[str, Any]:
        response: dict[str, Any] = self.gps_data.to_dict()
        response["message_type"] = self.message_type
        response["command"] = self.command
        return response

    def from_dict(self, data: dict[str, Any]) -> None:
        ### ! not working yet
        return super().from_dict(data)
