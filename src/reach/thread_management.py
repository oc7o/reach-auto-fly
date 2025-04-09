import logging
import queue

from dronekit import Vehicle

message_queues = {
    "mqtt_listener_daemon": queue.Queue(),
    "flight_controller_daemon": queue.Queue(),
    "recognition_model_daemon": queue.Queue(),
}

loggers = {
    "main": logging.getLogger("main"),
    "flight_controller_daemon": logging.getLogger("flight_controller_daemon"),
    "recognition_model_daemon": logging.getLogger("recognition_model_daemon"),
}

for logger in loggers:
    loggers[logger].propagate = False


class DroneState:
    emergency = False
    hold_postion = [False, ""]
    vehicle: Vehicle | None = None


drone_state = DroneState()
