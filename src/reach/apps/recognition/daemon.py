from logging import Logger, getLogger

import tensorflow as tf
import torch
import torchreid
from cv2 import VideoCapture
from mediapipe.python.solutions.pose import Pose

from reach.apps.recognition.recognition import run_model


def recognition_model_daemon():
    logger: Logger = getLogger("recognition_model_daemon")

    ## Load Camera Streams
    camera0: VideoCapture = VideoCapture(0)

    logger.info("loaded camera")

    ## Load Models
    ### Load pre-trained model for general object detection
    object_detector = tf.saved_model.load(
        "./src/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/saved_model"
    )  # ? Which Type is this???
    logger.info("loaded general object detection model")

    # Load pre-trained model for pose estimation
    # mp_draw = mp.solutions.drawing_utils
    pose: Pose = Pose()

    logger.info("loaded pose estimation model")

    # Load pre-trained model for reidentification
    reid_model: torch.nn.Module = torchreid.models.build_model(
        name="osnet_x1_0",
        num_classes=1000,  # Number of people in the dataset it was trained on
        pretrained=True,
    )
    reid_model.eval()

    logger.info("loaded re-id model")

    # >>> RUNNING MODEL
    run_model(object_detector, camera0, pose, reid_model)
    # <<<

    # CLEAN UP?
    camera0.release()
