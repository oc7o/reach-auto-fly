import collections
import collections.abc
import sys
import threading
import time

import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import paho.mqtt.client as mqtt
import torchreid


def patch_asscalar(a):
    return a.item()


setattr(np, "asscalar", patch_asscalar)

# import serial
import tensorflow as tf

collections.MutableMapping = collections.abc.MutableMapping

from dronekit import VehicleMode, connect

from reach.config import BROKER_IP
from reach.flight_controller import arm_and_takeoff, land
from reach.mqtt import on_connect, on_message
from reach.recognition import run_model
from reach.thread_management import drone_state, message_queues
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


# def hold_postion_daemon():
#     while True:
#         if drone_state.hold_postion:
#             drone_state.vehicle.mode = VehicleMode("PosHold")


def emergency_daemon():
    while True:
        if drone_state.vehicle == None:
            print("Vehicle not initialized.")
        if drone_state.emergency:
            drone_state.vehicle.mode = VehicleMode("LAND")
            while drone_state.vehicle.mode != "LAND":
                print("Waiting for drone to enter LAND mode")
                time.sleep(1)
            print("Vehicle now in LAND mode. Will touch ground shortly.")
            sys.exit()
        time.sleep(0.1)


def flight_controller_daemon():

    msg_queue = message_queues["flight_controller_daemon"]
    while True:
        if not msg_queue.empty():
            message = msg_queue.get()
            if message == "takeUp":
                arm_and_takeoff(drone_state.vehicle, 1)
            elif message == "land":
                land(drone_state.vehicle)
            elif message == "holdPisition":
                drone_state.vehicle.mode = VehicleMode("PosHold")


def mqtt_listener_daemon():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_IP, 1883, 60)
    client.loop_forever()  # Lässt den Client dauerhaft laufen


def recognition_model_daemon():
    ## Load Camera Streams
    camera0: cv2.VideoCapture = cv2.VideoCapture(0)

    ## Load Models
    ### Load pre-trained model for general object detection
    object_detector = tf.saved_model.load(
        "../src/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model"
    )

    # Load pre-trained model for pose estimation
    mp_pose = mp.solutions.pose
    # mp_draw = mp.solutions.drawing_utils
    pose = mp_pose.Pose()

    # Load pre-trained model for reidentification
    reid_model = torchreid.models.build_model(
        name="osnet_x1_0",
        num_classes=1000,  # Number of people in the dataset it was trained on
        pretrained=True,
    )
    reid_model.eval()

    # >>> RUNNING MODEL
    run_model(object_detector, camera0, mp_pose, pose, reid_model)
    # <<<

    # CLEAN UP?
    camera0.release()


def main():
    drone_state.vehicle = connect("/dev/ttyACM0", baud=57600, wait_ready=True)

    # Start threads
    mqtt_thread = threading.Thread(target=mqtt_listener_daemon, daemon=True)
    flight_controller_thread = threading.Thread(
        target=flight_controller_daemon, daemon=True
    )
    emergency_thread = threading.Thread(target=emergency_daemon, daemon=True)

    recognition_thread = threading.Thread(target=recognition_model_daemon, daemon=True)

    mqtt_thread.start()
    flight_controller_thread.start()
    recognition_thread.start()

    mqtt_thread.join()
    flight_controller_thread.join()
    recognition_thread.join()

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
