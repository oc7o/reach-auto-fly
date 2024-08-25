import serial
import cv2
import base64

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

import time


# LoRa-Transmitter-Setup
port = "/dev/ttyUSB0"  # Replace with your serial port
baud_rate = 115200  # Replace with your baud rate

# Create a serial object
lora_device = serial.Serial(port, baud_rate)