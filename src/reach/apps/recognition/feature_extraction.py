import numpy as np
from mediapipe.python.solutions.pose import PoseLandmark

from reach.utils.colors import most_common_pixel


def get_person_properties(
    image_rgb: np.ndarray, landmarks
) -> dict[str, tuple[int, int, int]] | None:
    # image_rgb = reduce_colors(image_rgb)
    # print(image_rgb.shape)

    # get tshirt color
    left_shoulder_x = int(
        landmarks[PoseLandmark.LEFT_SHOULDER.value].x * image_rgb.shape[1]
    )
    left_shoulder_y = int(
        landmarks[PoseLandmark.LEFT_SHOULDER.value].y * image_rgb.shape[0]
    )
    right_shoulder_x = int(
        landmarks[PoseLandmark.RIGHT_SHOULDER.value].x * image_rgb.shape[1]
    )
    right_shoulder_y = int(
        landmarks[PoseLandmark.RIGHT_SHOULDER.value].y * image_rgb.shape[0]
    )

    left_hip_x = int(
        landmarks[PoseLandmark.LEFT_HIP.value].x * image_rgb.shape[1]
    )
    left_hip_y = int(
        landmarks[PoseLandmark.LEFT_HIP.value].y * image_rgb.shape[0]
    )
    right_hip_x = int(
        landmarks[PoseLandmark.RIGHT_HIP.value].x * image_rgb.shape[1]
    )
    right_hip_y = int(
        landmarks[PoseLandmark.RIGHT_HIP.value].y * image_rgb.shape[0]
    )

    min_x = min([left_hip_x, right_hip_x, left_shoulder_x, right_shoulder_x])
    max_x = max([left_hip_x, right_hip_x, left_shoulder_x, right_shoulder_x])
    min_y = min([left_hip_y, right_hip_y, left_shoulder_y, right_shoulder_y])
    max_y = max([left_hip_y, right_hip_y, left_shoulder_y, right_shoulder_y])

    if (
        max_x > image_rgb.shape[1]
        or max_y > image_rgb.shape[0]
        or min_x < 0
        or min_y < 0
    ):
        return None

    tshirt = image_rgb[min_y : max_y + 1, min_x : max_x + 1]

    # plt.imshow(tshirt)
    # plt.show()

    tshirt_color = most_common_pixel(tshirt)

    # get pants
    left_knee_x = int(
        landmarks[PoseLandmark.LEFT_KNEE.value].x * image_rgb.shape[1]
    )
    left_knee_y = int(
        landmarks[PoseLandmark.LEFT_KNEE.value].y * image_rgb.shape[0]
    )

    min_x = min([left_hip_x, left_knee_x])
    max_x = max([left_hip_x, left_knee_x])
    min_y = min([left_hip_y, left_knee_y])
    max_y = max([left_hip_y, left_knee_y])

    if (
        max_x > image_rgb.shape[1]
        or max_y > image_rgb.shape[0]
        or min_x < 0
        or min_y < 0
    ):
        return None

    pants = image_rgb[
        min_y : max_y + 1, min_x : max_x + 1
    ]  # TODO: maybe compare with right leg?

    pants_color = most_common_pixel(pants)

    return {"tshirt_color": tshirt_color, "pants_color": pants_color}
