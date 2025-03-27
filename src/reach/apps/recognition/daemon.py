import cv2
import mediapipe as mp
import tensorflow as tf
import torchreid

from reach.apps.recognition.recognition import run_model


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
