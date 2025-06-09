from uuid import UUID, uuid4

import numpy as np
import torch
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor
from PIL import Image
from torch import Tensor
from torchvision import transforms

from reach.apps.flight_controller.gps_data import GPSData
from reach.config import (
    MAX_PANTS_COLOR_DELTA,
    MAX_PERSON_DATA_LIST_ENTRIES,
    MAX_TSHIRT_COLOR_DELTA,
    MIN_PERSON_COMPARISON_MATCH_LEVEL_1,
    MIN_PERSON_COMPARISON_MATCH_LEVEL_2,
)
from reach.utils.colors import average_color


class Person:
    """
    Which properties are relevant for uniquely identifying a person?
    - tshirt_color
    - pants_color
    - relative_position_in_frame
    - person_reid_model (for reidentification)

    - shoe_color?
    - face_landmarks???
    """

    uuid: UUID
    all_box_dimensions: list[list[int]] = []  # ymin,xmin,ymax,xmax
    tshirt_colors: list[tuple[int, int, int]]
    pants_colors: list[tuple[int, int, int]]
    first_seen: float  # time.time()
    last_seen: float  # time.time()
    gps_location: GPSData
    person_image: np.ndarray | None = None
    recognition_accuracy: float

    def __init__(
        self,
        box_dimensions,
        tshirt_color: tuple[int, int, int] | None,
        pants_color: tuple[int, int, int] | None,
        person_image: np.ndarray,
        recognition_accuracy: float,
        first_seen: float,
        gps_location: GPSData,
    ):
        self.uuid = uuid4()
        self.all_box_dimensions.append(box_dimensions)
        self.tshirt_colors = []
        if tshirt_color:
            self.tshirt_colors.append(tshirt_color)
        self.pants_colors = []
        if pants_color:
            self.pants_colors.append(pants_color)
        self.person_image = person_image
        self.recognition_accuracy = recognition_accuracy
        self.first_seen = first_seen
        self.gps_location = gps_location

    def __str__(self) -> str:
        return str(self.uuid)

    def __repr__(self) -> str:
        return str(self.uuid)

    def get_average_tshirt_color(self):
        return average_color(self.tshirt_colors)

    def get_average_pants_color(self):
        return average_color(self.pants_colors)

    def get_last_box_dimensions(self):
        """
        returns
            - height
            - width
            - center_x
            - center_y
        """
        pass

    def clean_up(self) -> None:
        if len(self.tshirt_colors) > MAX_PERSON_DATA_LIST_ENTRIES:
            del self.tshirt_colors[0]
        if len(self.pants_colors) > MAX_PERSON_DATA_LIST_ENTRIES:
            del self.pants_colors[0]


def image_transform(image: np.ndarray) -> Tensor:
    transform: transforms.Compose = transforms.Compose(
        [
            transforms.Resize((256, 128)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )

    img_t: Tensor = transform(Image.fromarray(image))  # type: ignore

    return img_t


def check_if_such_person_exists(
    person_table: list[Person],
    tshirt_color: tuple[int, int, int] | None,
    pants_color: tuple[int, int, int] | None,
    box_dimensions: tuple[int, int, int, int],
    compareable_image: np.ndarray,
    reid_model: torch.nn.Module,
) -> tuple[bool, Person | None]:
    for person in person_table:
        similiarty_points: int = 0
        # check color distance
        # tshirt

        if tshirt_color and len(person.tshirt_colors) > 0:
            # person_colror
            person_tshirt_color: sRGBColor = sRGBColor(
                *person.get_average_tshirt_color(), is_upscaled=True
            )
            #
            compareable_tshirt_color: sRGBColor = sRGBColor(
                *tshirt_color, is_upscaled=True
            )

            # Convert from RGB to Lab Color Space
            color1_lab: LabColor = convert_color(person_tshirt_color, LabColor)  # type: ignore
            color2_lab: LabColor = convert_color(
                compareable_tshirt_color, LabColor
            )  # type: ignore

            delta_e = delta_e_cie2000(color1_lab, color2_lab)

            # print(delta_e)

            if delta_e < MAX_TSHIRT_COLOR_DELTA:
                similiarty_points += 1

        if pants_color and len(person.pants_colors) > 0:
            # pants
            person_pants_color = sRGBColor(
                *person.get_average_pants_color(), is_upscaled=True
            )
            #
            compareable_pants_color = sRGBColor(*pants_color, is_upscaled=True)

            # Convert from RGB to Lab Color Space
            color1_lab = convert_color(person_pants_color, LabColor)  # type: ignore
            color2_lab = convert_color(compareable_pants_color, LabColor)  # type: ignore

            delta_e = delta_e_cie2000(color1_lab, color2_lab)

            # print(delta_e)

            if delta_e < MAX_PANTS_COLOR_DELTA:
                similiarty_points += 1

        # TODO:
        # check_box_size
        # check_box_position

        # check compareable image

        if person.person_image is not None:
            img1: Tensor = image_transform(person.person_image).unsqueeze(
                0
            )  # Add batch dimension
            img2: Tensor = image_transform(compareable_image).unsqueeze(0)

            # Extract feature embeddings
            with torch.no_grad():
                feat1 = reid_model(img1)
                feat2 = reid_model(img2)

            # Compare features using cosine similarity or Euclidean distance
            cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
            similarity = cos(feat1, feat2).item()

            if similarity > MIN_PERSON_COMPARISON_MATCH_LEVEL_1:
                similiarty_points += 2
            elif similarity > MIN_PERSON_COMPARISON_MATCH_LEVEL_2:
                similiarty_points += 1

        # Conclusion
        if similiarty_points >= 2:  # normally 4
            return (True, person)
        else:
            continue
    return (False, None)


def get_least_accuracy_person(
    person_table: list[Person],
) -> tuple[Person | None, int]:
    least_accuracy: float = 1
    least_accuracy_person: Person = person_table[0]
    table_id: int = 0

    for person_id, person in enumerate(person_table):
        if person.recognition_accuracy < least_accuracy:
            least_accuracy = person.recognition_accuracy
            least_accuracy_person = person
            table_id = person_id
    return least_accuracy_person, table_id
