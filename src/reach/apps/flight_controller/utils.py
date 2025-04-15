from reach.thread_management import drone_state, loggers


def drone_is_initialized():
    if drone_state.vehicle is None:
        loggers["flight_controller_daemon"].warning(
            "Connection to flight controller not initialized, unable to perform actions on vehicle"
        )
        return False
    return True
