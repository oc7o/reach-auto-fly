import logging
from queue import Queue

from dronekit import Vehicle
from paho.mqtt.client import Client

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
    emergency: bool = False
    hold_postion: tuple[bool, str] = (False, "")
    vehicle: Vehicle | None = None
    mqtt_client: Client | None = None
    gps_location: dict[str, float | None] | None = None


drone_state: DroneState = DroneState()
