from typing import Any, ClassVar, Dict

from dronekit import LocationGlobalRelative
from typing_extensions import AnyStr

from reach.apps.mqtt.message import Message
from reach.thread_management import DroneState


class GotoLocation(Message):
    message_type: ClassVar[str] = "command"
    command: ClassVar[str] = "goto_location"

    def to_dict(self) -> Dict[str, Any]:
        return super().to_dict()

    def from_dict(self, data: Dict[str, Any]) -> None:
        return super().from_dict(data)

    @classmethod
    def handle_command(cls, cmd: Dict[str, AnyStr]) -> None:
        assert DroneState.vehicle is not None
        DroneState.vehicle.simple_goto(
            location=LocationGlobalRelative(
                cmd["lat"], cmd["lon"], cmd.get("alt", 0.0)
            )
        )
