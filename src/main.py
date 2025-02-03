import collections
import collections.abc
import threading

import cv2
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as mqtt

# import serial
import tensorflow as tf

collections.MutableMapping = collections.abc.MutableMapping

from dronekit import connect

from reach.config import BROKER_IP
from reach.flight_controller import arm_and_takeoff, land
from reach.mqtt import on_connect, on_message
from reach.thread_management import message_queues
from reach.utils.camera import format_image, take_photo

# # LoRa-Transmitter-Setup
# port = "/dev/ttyUSB0"  # Replace with your serial port
# baud_rate = 115200  # Replace with your baud rate

# # Create a serial object
# lora_device = serial.Serial(port, baud_rate)


# camera0 = cv2.VideoCapture(0)

# detector = tf.saved_model.load(
#     "./ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model"
# )


def flight_controller_daemon():
    vehicle = connect("/dev/ttyACM0", baud=57600, wait_ready=True)

    msg_queue = message_queues["flight_controller_daemon"]
    while True:
        if not msg_queue.empty():
            message = msg_queue.get()
            if message == "takeUp":
                arm_and_takeoff(vehicle, 1)
            if message == "land":
                land(vehicle)


def mqtt_listener_daemon():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_IP, 1883, 60)
    client.loop_forever()  # Lässt den Client dauerhaft laufen


def recognition_model_daemon():
    pass


def main():

    # Start threads
    mqtt_thread = threading.Thread(target=mqtt_listener_daemon, daemon=True)
    flight_controller_thread = threading.Thread(
        target=flight_controller_daemon, daemon=True
    )

    mqtt_thread.start()
    flight_controller_thread.start()

    mqtt_thread.join()
    flight_controller_thread.join()

    # # take picture
    # frame = take_photo(camera0)
    # # format image
    # frame = format_image(frame)

    # result = detector(img)
    # result = {key: value.numpy() for key, value in result.items()}

    # for i in range(len(result["detection_classes"][0])):
    #     detected = result["detection_classes"][0][i]
    #     accuracy = result["detection_scores"][0][i]
    #     if detected == 1 and accuracy > 0.75:
    #         print("Person found at location", vehicle.location.global_frame)


if __name__ == "__main__":
    main()
