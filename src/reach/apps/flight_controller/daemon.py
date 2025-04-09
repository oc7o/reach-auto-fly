import logging

from dronekit import VehicleMode, connect

from reach.apps.flight_controller.flight_controller import arm_and_takeoff, land
from reach.apps.flight_controller.utils import check_if_drone_is_initialized
from reach.thread_management import drone_state, message_queues


def flight_controller_daemon():

    check_if_drone_is_initialized()

    msg_queue = message_queues["flight_controller_daemon"]
    while True:
        if drone_state.vehicle is None:
            # print("Waiting for drone intitlization")
            pass
        elif not msg_queue.empty():
            message = msg_queue.get()
            if message == "takeUp":
                arm_and_takeoff(drone_state.vehicle, 1)
            elif message == "land":
                land(drone_state.vehicle)
            elif message == "holdPisition":
                drone_state.vehicle.mode = VehicleMode("PosHold")
