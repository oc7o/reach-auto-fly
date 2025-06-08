import time
from logging import Logger, getLogger
from typing import Any, ClassVar, Dict

from dronekit import VehicleMode
from typing_extensions import AnyStr

from reach.apps.mqtt.message import Message
from reach.thread_management import DroneState


class LandCommand(Message):
    message_type: ClassVar[str] = "command"
    command: ClassVar[str] = "land"

    def to_dict(self) -> Dict[str, Any]:
        return super().to_dict()

    def from_dict(self, data: Dict[str, Any]) -> None:
        return super().from_dict(data)

    @classmethod
    def handle_command(cls, cmd: Dict[str, AnyStr]) -> None:
        assert DroneState.vehicle is not None

        logger: Logger = getLogger("flight_controller_daemon")

        DroneState.vehicle.mode = VehicleMode("LAND")
        while DroneState.vehicle.mode != "LAND":
            logger.info("Waiting for drone to enter LAND mode")
            time.sleep(1)
        logger.info("Vehicle now in LAND mode. Will touch ground shortly.")
        return

        # Land the vehicle
        # This will command the vehicle to land at its current location.
        DroneState.vehicle.mode = "LAND"
        DroneState.vehicle.armed = False
        # Alternatively, you can use the simple_land method if available.
        # DroneState.vehicle.simple_land()
