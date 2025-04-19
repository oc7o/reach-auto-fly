import logging
import queue

from dronekit import Vehicle
from paho.mqtt.client import Client

message_queues = {
    "mqtt_listener_daemon": queue.Queue(),
    "flight_controller_daemon": queue.Queue(),
    "recognition_model_daemon": queue.Queue(),
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
    emergency = False
    hold_postion = [False, ""]
    vehicle: Vehicle | None = None
    mqtt_client: Client | None = None


drone_state = DroneState()
