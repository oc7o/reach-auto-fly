from typing import Any, ClassVar, Dict

from dronekit import LocationGlobalRelative
from typing_extensions import AnyStr

from reach.apps.mqtt.message import Message
from reach.thread_management import DroneState


class RelativeMoveCommand(Message):
    message_type: ClassVar[str] = "command"
    command: ClassVar[str] = "relative_move"

    def to_dict(self) -> Dict[str, Any]:
        return super().to_dict()

    def from_dict(self, data: Dict[str, Any]) -> None:
        return super().from_dict(data)

    @classmethod
    def handle_command(cls, cmd: Dict[str, AnyStr]) -> None:
        assert DroneState.vehicle is not None

        x: float = float(cmd.get("x", 0.0))  # forward/backward movement
        y: float = float(cmd.get("y", 0.0))  # left/right movement
        z: float = float(cmd.get("z", 0.0))  # up/down movement

        # Get current GPS location
        current_location = DroneState.gps_location
        if current_location is None:
            raise ValueError("Current GPS location is not available.")

        # Calculate new GPS location based on relative movement
        # Assuming x and y are in meters, and z is in meters above the current altitude
        # This is a simplified calculation; in practice, you would need to account for the curvature of the Earth and other factors.
        new_lat = current_location.lat + (
            x / 111320
        )  # approx. meters to degrees
        new_lon = current_location.lon + (
            y / (111320 * abs(current_location.lat))
        )  # adjust for latitude
        new_alt = current_location.alt + z  # relative altitude change
        new_location = LocationGlobalRelative(new_lat, new_lon, new_alt)

        DroneState.vehicle.simple_goto(location=new_location)
