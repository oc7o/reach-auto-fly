import time
from logging import Logger, getLogger
from typing import Any, ClassVar, Dict

from dronekit import VehicleMode
from typing_extensions import AnyStr

from reach.apps.mqtt.message import Message
from reach.config import MAXIMUM_WAIT_COUNT
from reach.thread_management import DroneState


class TakeoffCommand(Message):
    message_type: ClassVar[str] = "command"
    command: ClassVar[str] = "takeoff"

    def to_dict(self) -> Dict[str, Any]:
        return super().to_dict()

    def from_dict(self, data: Dict[str, Any]) -> None:
        return super().from_dict(data)

    @classmethod
    def handle_command(cls, cmd: Dict[str, AnyStr]) -> None:
        assert DroneState.vehicle is not None

        # Extract the target altitude from the command
        # This assumes the command contains a key "alt" with the desired relative takeoff altitude in meters.
        # If the key is not present, it defaults to 10 meters.
        target_altitude: float = float(cmd.get("alt", 10.0))
        # # Takeoff the vehicle to the specified altitude
        # DroneState.vehicle.simple_takeoff(target_altitude)
        # # Wait until the vehicle reaches the target altitude
        # while True:

        """
        Arms vehicle and fly to aTargetAltitude.
        """
        logger: Logger = getLogger("flight_controller_daemon")

        logger.info("Executing basic pre-arm checks")

        wait_count: int = 0
        # Don't try to arm until autopilot is ready
        while not DroneState.vehicle.is_armable:
            if wait_count >= MAXIMUM_WAIT_COUNT:
                logger.error(
                    "Arming check timed out after {MAXIMUM_WAIT_COUNT}s"
                )
                raise Exception(
                    f"Arming check timed out after {MAXIMUM_WAIT_COUNT}s"
                )

            logger.info("Waiting for vehicle to initialise...")
            time.sleep(1)
            wait_count += 1

        logger.info("Arming motors")

        # Copter should arm in GUIDED mode
        DroneState.vehicle.mode = VehicleMode("GUIDED")
        DroneState.vehicle.armed = True

        wait_count = 0
        # Confirm vehicle armed before attempting to take off
        while not DroneState.vehicle.armed:
            if wait_count >= MAXIMUM_WAIT_COUNT:
                logger.error(f"Try to arm timed out after {wait_count}s")
                raise Exception("Try to arm timed out after {wait_count}s")
            logger.info("Waiting for arming...")
            time.sleep(1)

        logger.info("Taking off!")
        DroneState.vehicle.simple_takeoff(
            target_altitude
        )  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #  after Vehicle.simple_takeoff will execute immediately).
        # while True:
        #     print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        #     #Break and return from function just below target altitude.
        #     if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
        #         print("Reached target altitude")
        #         break
        #     time.sleep(1)

        return
