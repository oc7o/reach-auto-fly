import queue

from dronekit import Vehicle

message_queues = {
    "mqtt_listener_daemon": queue.Queue(),
    "flight_controller_daemon": queue.Queue(),
    "recognition_model_daemon": queue.Queue(),
}


class DroneState:
    emergency = False
    hold_postion = [False, ""]
    vehicle: Vehicle | None = None


drone_state = DroneState()
