import logging
import time
from logging import Logger, getLogger
from queue import Queue

from dronekit import LocationGlobal, LocationGlobalRelative, VehicleMode, connect

from reach.apps.flight_controller.flight_controller import arm_and_takeoff, land
from reach.apps.flight_controller.gps_data import GPSData
from reach.apps.flight_controller.utils import drone_is_initialized
from reach.thread_management import DroneState, message_queues
from src.reach.apps import mqtt
from src.reach.apps.mqtt.message.broadcasts.gps_data import GPSDataBroadcast
from src.reach.apps.mqtt.message.serialization import serialize_message
from src.reach.config import GPS_TOPIC


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
            assert DroneState.vehicle is not None  # * see drone_is_initialized()
            message: str = msg_queue.get()
            if message == "takeUp":
                arm_and_takeoff(DroneState.vehicle, 1)
            elif message == "land":
                land(DroneState.vehicle)
            elif message == "holdPisition":
                DroneState.vehicle.mode = VehicleMode("PosHold")
        elif time.time() - last_time > 0.1:  # 100ms TODO: config.py ?
            # Do things in spare time

            assert DroneState.vehicle is not None

            now = time.time()
            global_location: LocationGlobal = DroneState.vehicle.location.global_frame
            global_location_ra: LocationGlobalRelative = (
                DroneState.vehicle.location.global_relative_frame
            )
            statelites_visible: int | None = DroneState.vehicle.gps_0.satellites_visible

            gps_data = GPSData(
                {
                    "lat": global_location.lat,
                    "lon": global_location.lon,
                    "alt": global_location_ra.alt,  # relative
                    "alt_abs": global_location.alt,
                    "statelites_visible": statelites_visible,
                    "timestamp": now,
                }
            )
            DroneState.gps_location = gps_data
            gps_data_message: GPSDataBroadcast = GPSDataBroadcast(gps_data)
            assert DroneState.mqtt_client is not None
            DroneState.mqtt_client.publish(
                GPS_TOPIC, serialize_message(gps_data_message)
            )

            last_time = now
