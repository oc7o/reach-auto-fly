print("--- starting program ---")

### Begin Config ###
from src.reach.config import PERSON_RECOGNITION_ACCEPTANCE

# import os

# os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

### Begin Imports ###
print("--- beginning imports ---")

import sys
import time
import uuid

import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import tensorflow as tf
import torch
import torchreid
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor
from PIL import Image
from skimage import color, exposure, io
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from torchvision import transforms

from reach.feature_extraction import get_person_properties
from reach.person import Person, check_if_such_person_exists
from reach.utils.camera import format_image, take_photo
from reach.utils.colors import average_color, most_common_pixel, reduce_colors
from reach.utils.graphics import draw_bounding_box_on_image, draw_boxes


def patch_asscalar(a):
    return a.item()


setattr(np, "asscalar", patch_asscalar)

print("--- finished imports ---")
### End Imports ###

### Load Camera Stream

camera0 = cv2.VideoCapture("../tmp/test_video4.MOV")
# camera0 = cv2.VideoCapture(0)

# video = cv2.VideoWriter("./video.avi", cv2.VideoWriter_fourcc(*"MJPG"), 4, (640, 640))


### Load Models

detector = tf.saved_model.load(
    "../src/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model"
)

# Load pre-trained model for pose estimation
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Load pre-trained model for reidentification
reid_model = torchreid.models.build_model(
    name="osnet_x1_0",
    num_classes=1000,  # Number of people in the dataset it was trained on
    pretrained=True,
)
reid_model.eval()

print("--- finished loading models ---")
print("--- starting image detection ---")

#####################
### Begin Program ###
#####################

person_table = []

frame_count = 0
while True:
    print(frame_count)
    if frame_count >= 50:
        print(person_table)
        sys.exit()
    img = take_photo(camera0)
    if img is None:
        break
    img = format_image(img)

    result = detector(img)
    result = {key: value.numpy() for key, value in result.items()}

    person_count = 0
    for detected_object in range(result["detection_classes"].shape[1]):
        tshirt_color = None
        pants_color = None

        if (
            result["detection_classes"][0][detected_object] == 1
            and result["detection_scores"][0][detected_object]
            > PERSON_RECOGNITION_ACCEPTANCE
        ):
            ymin, xmin, ymax, xmax = tuple(
                result["detection_boxes"][0][detected_object]
            )

            detected_person_frame = img.reshape(640, 640, 3)[
                int(ymin * 640) : int(ymax * 640), int(xmin * 640) : int(xmax * 640)
            ].copy()

            # cv2.imwrite('results/frame_' + str(frame_count) + '_person_' + str(person_count) + '.jpg', cv2.cvtColor(detected_person_frame, cv2.COLOR_RGB2BGR))

            resulted_pose_landmarks = pose.process(detected_person_frame)

            if resulted_pose_landmarks.pose_landmarks:
                # mp_draw.draw_landmarks(detected_person_frame, resulted_pose_landmarks.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                landmarks = resulted_pose_landmarks.pose_landmarks.landmark

                res = get_person_properties(detected_person_frame, landmarks, mp_pose)
                if res == None:
                    continue

                tshirt_color = res["tshirt_color"]
                pants_color = res["pants_color"]

                # tshirt_color = cv2.cvtColor(np.array(res['tshirt_color']).reshape(1,1,3), cv2.COLOR_RGB2BGR)
                # pants_color = cv2.cvtColor(np.array(res['pants_color']).reshape(1,1,3), cv2.COLOR_RGB2BGR)
                # cv2.imwrite('results/frame_' + str(frame_count) + '_tshirt_color_of_person_' + str(person_count) + '.jpg', tshirt_color)
                # cv2.imwrite('results/frame_' + str(frame_count) + '_pants_color_of_person_' + str(person_count) + '.jpg', pants_color)

                # feature extraction done
                # evaluating features

                does_exist, person = check_if_such_person_exists(
                    person_table,
                    tshirt_color,
                    pants_color,
                    (ymin, xmin, ymax, xmax),
                    detected_person_frame,
                    reid_model,
                )

                if does_exist:
                    pass
                else:
                    if tshirt_color and pants_color:
                        person = Person(
                            (ymin, xmin, ymax, xmax),
                            tshirt_color,
                            pants_color,
                            detected_person_frame.copy(),
                        )
                        person_table.append(person)

                person_count += 1

    # TODO: clean up persons from person_table who haven't been seen in a while (add timestamps)

    image_with_boxes = draw_boxes(
        img.reshape(640, 640, 3),
        result["detection_boxes"][0],
        result["detection_classes"][0],
        result["detection_scores"][0],
        min_score=0.2,
    )

    # video.write(image_with_boxes)

    # image_with_boxes = draw_boxes(
    #   test.reshape(640,640,3), result["detection_boxes"][0],
    #   result["detection_classes"][0], result["detection_scores"][0])

    frame_count += 1


### Clean up ###

print(len(person_table))
print(person_table)

print("End")

camera0.release()
# video.release()
# cv2.destroyAllWindows()
