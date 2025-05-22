from typing import Optional

import cv2
import numpy as np
from cv2.typing import MatLike


def take_photo(camera: cv2.VideoCapture) -> MatLike | None:
    """Reads next frame from camera instance"""
    rval: bool
    frame: Optional[MatLike]
    rval, frame = camera.read()
    return frame


def format_image(image: MatLike) -> np.ndarray:
    # ? Should this have a return type? Is None enough?
    # TODO: look above up (regarding side-effects)
    """Formats the image for right reach processing"""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = image.reshape(1,640,640,3)
    image = cv2.resize(image, (640, 640))
    image_np: np.ndarray = np.array(image)
    image_np = image_np.reshape(1, 640, 640, 3)
    return image_np
