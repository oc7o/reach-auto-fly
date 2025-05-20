import time
from logging import Logger, getLogger
from typing import NoReturn

from dronekit import LocationGlobalRelative, Vehicle, VehicleMode

from reach.config import MAXIMUM_WAIT_COUNT


def arm_and_takeoff(vehicle: Vehicle, aTargetAltitude: int) -> None:
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    logger: Logger = getLogger("flight_controller_daemon")

    logger.info("Executing basic pre-arm checks")

    wait_count: int = 0
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        if wait_count >= MAXIMUM_WAIT_COUNT:
            logger.error("Arming check timed out after {MAXIMUM_WAIT_COUNT}s")
            raise Exception(f"Arming check timed out after {MAXIMUM_WAIT_COUNT}s")

        logger.info("Waiting for vehicle to initialise...")
        time.sleep(1)
        wait_count += 1

    logger.info("Arming motors")

    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    wait_count = 0
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        if wait_count >= MAXIMUM_WAIT_COUNT:
            logger.error(f"Try to arm timed out after {wait_count}s")
            raise Exception("Try to arm timed out after {wait_count}s")
        logger.info("Waiting for arming...")
        time.sleep(1)

    logger.info("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

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


def land(vehicle: Vehicle) -> None:
    logger: Logger = getLogger("flight_controller_daemon")

    vehicle.mode = VehicleMode("LAND")
    while vehicle.mode != "LAND":
        logger.info("Waiting for drone to enter LAND mode")
        time.sleep(1)
    logger.info("Vehicle now in LAND mode. Will touch ground shortly.")
    return


# def hold_postion(vehicle: Vehicle) -> None:
#     latitude: float = vehicle.location.global_relative_frame.lat
#     longitude: float = vehicle.location.global_relative_frame.lon
#     altitude = None

#     a_location = LocationGlobalRelative(latitude, longitude, altitude)
