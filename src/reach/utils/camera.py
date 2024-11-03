import cv2
import numpy as np


def take_photo(camera):
    """Reads next frame from camera instance"""
    rval, frame = camera.read()
    return frame


def format_image(image):
    """Formats the image for right reach processing"""
    image_copy = image.copy()
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
    # image = image.reshape(1,640,640,3)
    image_copy = cv2.resize(image_copy, (640, 640))
    image_copy = np.array(image_copy)
    image_copy = image_copy.reshape(1, 640, 640, 3)
    return image_copy.copy()
