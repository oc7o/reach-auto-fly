import logging
import time
from logging import Logger, getLogger
from queue import Queue

from dronekit import LocationGlobal, LocationGlobalRelative, VehicleMode, connect

from reach.apps.flight_controller.flight_controller import arm_and_takeoff, land
from reach.apps.flight_controller.utils import drone_is_initialized
from reach.thread_management import drone_state, message_queues


def flight_controller_daemon() -> None:
    logger: Logger = getLogger("flight_controller_daemon")

    drone_is_initialized()

    msg_queue: Queue = message_queues["flight_controller_daemon"]

    last_time: float = time.time()

    while True:
        if not drone_is_initialized():
            # print("Waiting for drone intitlization")
            pass
        elif not msg_queue.empty():
            assert drone_state.vehicle is not None  # * see drone_is_initialized()
            message: str = msg_queue.get()
            if message == "takeUp":
                arm_and_takeoff(drone_state.vehicle, 1)
            elif message == "land":
                land(drone_state.vehicle)
            elif message == "holdPisition":
                drone_state.vehicle.mode = VehicleMode("PosHold")
        elif time.time() - last_time > 0.1:  # 100ms TODO: config.py ?
            # Do things in spare time

            assert drone_state.vehicle is not None

            now = time.time()
            global_location: LocationGlobal = drone_state.vehicle.location.global_frame
            global_location_ra: LocationGlobalRelative = (
                drone_state.vehicle.location.global_relative_frame
            )
            statelites_visible: int | None = (
                drone_state.vehicle.gps_0.satellites_visible
            )

            drone_state.gps_location = {
                "lat": global_location.lat,
                "lon": global_location.lon,
                "alt": global_location_ra.alt,  # relative
                "alt_abs": global_location.alt,
                "statelites_visible": statelites_visible,
                "timestamp": now,
            }

            last_time = now
