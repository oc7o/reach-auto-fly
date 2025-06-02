import logging
from queue import Queue
from typing import ClassVar

from dronekit import Vehicle
from paho.mqtt.client import Client

from reach.apps.flight_controller.gps_data import GPSData

message_queues: dict[str, Queue] = {
    "mqtt_listener_daemon": Queue(),
    "flight_controller_daemon": Queue(),
    "recognition_model_daemon": Queue(),
}

# loggers = {
#     "main": logging.getLogger("main"),
#     "mqtt_listener_daemon": logging.getLogger("mqtt_listener_daemon"),
#     "flight_controller_daemon": logging.getLogger("flight_controller_daemon"),
#     "recognition_model_daemon": logging.getLogger("recognition_model_daemon"),
# }

# for logger in loggers:
#     loggers[logger].propagate = False


class DroneState:
    emergency: ClassVar[bool] = False
    hold_postion: ClassVar[tuple[bool, str]] = (False, "")
    vehicle: ClassVar[Vehicle | None] = None
    mqtt_client: ClassVar[Client | None] = None
    gps_location: ClassVar[GPSData | None] = None
