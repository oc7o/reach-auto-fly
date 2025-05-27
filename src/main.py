import collections
import collections.abc
import logging
import sys
import threading
import time
from threading import Thread

import matplotlib.pyplot as plt
import numpy as np
from serial.serialutil import SerialException


def patch_asscalar(a):
    return a.item()


setattr(np, "asscalar", patch_asscalar)

collections.MutableMapping = collections.abc.MutableMapping

from dronekit import VehicleMode, connect

from reach.apps.flight_controller.daemon import flight_controller_daemon
from reach.apps.mqtt.daemon import mqtt_listener_daemon
from reach.apps.recognition.daemon import recognition_model_daemon
from reach.config import BROKER_IP
from reach.thread_management import drone_state
from reach.utils.camera import format_image, take_photo


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s",
        handlers=[logging.StreamHandler()],
    )

    logger: logging.Logger = logging.getLogger("main")

    try:
        drone_state.vehicle = connect("/dev/ttyACM0", baud=57600, wait_ready=True)
    except (FileNotFoundError, SerialException) as e:
        logger.warning("Could not connect to vehicle flight controller")

    # Start threads
    mqtt_thread: Thread = Thread(target=mqtt_listener_daemon, daemon=True)
    flight_controller_thread: Thread = Thread(
        target=flight_controller_daemon, daemon=True
    )
    # emergency_thread = threading.Thread(target=emergency_daemon, daemon=True)

    recognition_thread: Thread = Thread(target=recognition_model_daemon, daemon=True)

    mqtt_thread.start()
    flight_controller_thread.start()
    recognition_thread.start()

    mqtt_thread.join()
    flight_controller_thread.join()
    recognition_thread.join()


if __name__ == "__main__":
    main()
