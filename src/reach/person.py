from uuid import UUID, uuid4

import numpy as np
import torch
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor
from PIL import Image
from torchvision import transforms

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
    tshirt_colors: list[list[int]]
    pants_colors: list[list[int]]
    first_seen: float  # time.time()
    last_seen: float  # time.time()
    person_image: np.ndarray | None = None
    recognition_accuracy: float

    def __init__(
        self,
        box_dimensions,
        tshirt_color,
        pants_color,
        person_image,
        recognition_accuracy,
    ):
        self.uuid = uuid4()
        self.all_box_dimensions.append(box_dimensions)
        self.tshirt_colors = [tshirt_color]
        self.pants_colors = [pants_color]
        self.person_image = person_image
        self.recognition_accuracy = recognition_accuracy

    def __str__(self):
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


def check_if_such_person_exists(
    person_table: list,
    tshirt_color,
    pants_color,
    box_dimensions,
    compareable_image,
    reid_model,
):
    for person in person_table:
        similiarty_points = 0
        # check color distance
        # tshirt

        if tshirt_color:
            # person_colror
            person_tshirt_color = sRGBColor(
                *person.get_average_tshirt_color(), is_upscaled=True
            )
            #
            compareable_tshirt_color = sRGBColor(*tshirt_color, is_upscaled=True)

            # Convert from RGB to Lab Color Space
            color1_lab = convert_color(person_tshirt_color, LabColor)
            color2_lab = convert_color(compareable_tshirt_color, LabColor)

            delta_e = delta_e_cie2000(color1_lab, color2_lab)

            # print(delta_e)

            if delta_e < 10:
                similiarty_points += 1

        if pants_color:
            # pants
            person_pants_color = sRGBColor(
                *person.get_average_pants_color(), is_upscaled=True
            )
            #
            compareable_pants_color = sRGBColor(*pants_color, is_upscaled=True)

            # Convert from RGB to Lab Color Space
            color1_lab = convert_color(person_pants_color, LabColor)
            color2_lab = convert_color(compareable_pants_color, LabColor)

            delta_e = delta_e_cie2000(color1_lab, color2_lab)

            # print(delta_e)

            if delta_e < 10:
                similiarty_points += 1

        # TODO:
        # check_box_size
        # check_box_position

        # check compareable image

        transform = transforms.Compose(
            [
                transforms.Resize((256, 128)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        img1 = transform(Image.fromarray(person.person_image)).unsqueeze(
            0
        )  # Add batch dimension
        img2 = transform(Image.fromarray(compareable_image)).unsqueeze(0)

        # Extract feature embeddings
        with torch.no_grad():
            feat1 = reid_model(img1)
            feat2 = reid_model(img2)

        # Compare features using cosine similarity or Euclidean distance
        cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        similarity = cos(feat1, feat2).item()

        if similarity > 0.9:
            similiarty_points += 2
        elif similarity > 0.8:
            similiarty_points += 1

        # Conclusion
        if similiarty_points >= 2:  # normally 4
            return (True, person)
        else:
            continue
    return (False, None)
