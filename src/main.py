import collections
import collections.abc
import logging
from threading import Thread

import numpy as np
from serial.serialutil import SerialException


def patch_asscalar(a):
    return a.item()


setattr(np, "asscalar", patch_asscalar)

collections.MutableMapping = collections.abc.MutableMapping


import dronekit as _  # noqa: F401
from dronekit import connect

from reach.apps.flight_controller.daemon import flight_controller_daemon
from reach.apps.mqtt.daemon import mqtt_listener_daemon
from reach.apps.recognition.daemon import recognition_model_daemon
from reach.thread_management import DroneState


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s",
        handlers=[logging.StreamHandler()],
    )

    logger: logging.Logger = logging.getLogger("main")

    try:
        DroneState.vehicle = connect(
            "/dev/ttyACM0", baud=57600, wait_ready=True
        )
    except (FileNotFoundError, SerialException):
        logger.warning("Could not connect to vehicle flight controller")

    # Start threads
    mqtt_thread: Thread = Thread(target=mqtt_listener_daemon, daemon=True)
    flight_controller_thread: Thread = Thread(
        target=flight_controller_daemon, daemon=True
    )
    # emergency_thread = threading.Thread(target=emergency_daemon, daemon=True)

    recognition_thread: Thread = Thread(
        target=recognition_model_daemon, daemon=True
    )

    mqtt_thread.start()
    flight_controller_thread.start()
    recognition_thread.start()

    mqtt_thread.join()
    flight_controller_thread.join()
    recognition_thread.join()


if __name__ == "__main__":
    main()
