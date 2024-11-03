import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial
import tensorflow as tf
from dronekit import connect

from src.reach.utils.camera import format_image, take_photo

# # LoRa-Transmitter-Setup
# port = "/dev/ttyUSB0"  # Replace with your serial port
# baud_rate = 115200  # Replace with your baud rate

# # Create a serial object
# lora_device = serial.Serial(port, baud_rate)


camera0 = cv2.VideoCapture(0)

detector = tf.saved_model.load(
    "./ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model"
)

vehicle = connect("/dev/ttyACM0", wait_ready=True)


def main():
    # take picture
    frame = take_photo(camera0)
    # format image
    frame = format_image(frame)

    result = detector(img)
    result = {key: value.numpy() for key, value in result.items()}

    for i in range(len(result["detection_classes"][0])):
        detected = result["detection_classes"][0][i]
        accuracy = result["detection_scores"][0][i]
        if detected == 1 and accuracy > 0.75:
            print("Person found at location", vehicle.location.global_frame)


if __name__ == "__main__":
    main()
