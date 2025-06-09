from typing import Any, ClassVar, Dict

from dronekit import VehicleMode
from typing_extensions import AnyStr

from reach.apps.mqtt.message import Message
from reach.thread_management import DroneState


class HoldPositionCommand(Message):
    message_type: ClassVar[str] = "command"
    command: ClassVar[str] = "hold_position"

    def to_dict(self) -> Dict[str, Any]:
        return super().to_dict()

    def from_dict(self, data: Dict[str, Any]) -> None:
        return super().from_dict(data)

    @classmethod
    def handle_command(cls, cmd: Dict[str, AnyStr]) -> None:
        assert DroneState.vehicle is not None

        DroneState.vehicle.mode = VehicleMode("LOITER")
