import serial
import cv2
import base64
import atexit
import time

import tensorflow as tf

import matplotlib.pyplot as plt
# import tempfile
# from six.moves.urllib.request import urlopen
# from six import BytesIO

import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from dronekit import connect

from reach.camera import take_photo, format_image

# LoRa-Transmitter-Setup
port = "/dev/ttyUSB0"  # Replace with your serial port
baud_rate = 115200  # Replace with your baud rate

# Create a serial object
lora_device = serial.Serial(port, baud_rate)

camera0 = cv2.VideoCapture(0)

detector = tf.saved_model.load("../ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model")

vehicle = connect("/dev/ttyACM0", wait_ready=True)

def main():
    # take picture
    frame = take_photo(camera0)
    # format image
    frame = format_image(frame)

    result = detector(img)
    result = {key:value.numpy() for key,value in result.items()}

    for i in range(len(result['detection_classes'][0])):
        detected = result['detection_classes'][0][i]
        accuracy = result['detection_scores'][0][i]
        if detected == 1 and accuracy > 0.75:
            print("Person found at location", vehicle.location.global_frame)

# def exit_handler():
#     print 'My application is ending!'

# atexit.register(exit_handler)

    
if __name__ == "__main__":
    main()