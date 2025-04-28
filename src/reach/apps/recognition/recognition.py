import logging
import time
from typing import Any

from reach.apps.mqtt.mqtt import send_message, send_response
from reach.apps.recognition.feature_extraction import get_person_properties
from reach.apps.recognition.person import (
    Person,
    check_if_such_person_exists,
    get_least_accuracy_person,
)
from reach.config import MAX_PERSONS_TRACKED, PERSON_RECOGNITION_ACCEPTANCE
from reach.thread_management import drone_state
from reach.utils.camera import format_image, take_photo


def send_found_person(
    pants_color, tshirt_color, image_of_person, recognition_accuracy, found_timestamp
):
    send_messages = True
    vehicle_access = True
    msg: dict[str, Any] = {"type": "found_person"}

    mqtt_client = drone_state.mqtt_client
    if mqtt_client is None:
        send_messages = False
        logging.getLogger("mqtt_listener_daemon").error("❌ No mqtt connection")

    vehicle = drone_state.vehicle
    if vehicle is None:
        vehicle_access = False
        logging.getLogger("flight_controller_daemon").error("❌ No vehicle connection")

    if vehicle_access:
        ### TODO: GPS will be integrated into the recognition model as metadata
        global_location = vehicle.location.global_frame
        global_location_ra = vehicle.location.global_relative_frame
        statelites_visible = vehicle.gps_0.satellites_visible
        ###
        msg["lat"] = global_location.lat
        msg["lon"] = global_location.lon
        msg["alt"] = global_location_ra.alt  # relative
        msg["alt_abs"] = global_location.alt
        msg["statelites_visible"] = statelites_visible

    msg["vehicle_access"] = vehicle_access
    msg["recognition_accuracy"] = recognition_accuracy
    msg["found_timestamp"] = found_timestamp
    logging.debug("colors")
    logging.debug(pants_color)
    logging.debug(tshirt_color)
    logging.debug(
        # image_of_person,
        recognition_accuracy,
    )
    logging.debug(found_timestamp)

    # idk
    # logging.getLogger("")
    if send_messages:
        send_response(mqtt_client, msg)


def run_model(object_detector, camera, mp_pose, pose, reid_model):
    person_table = []

    while True:
        img = None
        img = take_photo(camera)
        time_after_photo = time.time()
        if img is None:
            logging.getLogger("recognition_model_daemon").error(
                "Error reading video stream"
            )
            break
        img = format_image(img)

        result = object_detector(img)
        result = {key: value.numpy() for key, value in result.items()}

        for detected_object in range(result["detection_classes"].shape[1]):
            tshirt_color = None
            pants_color = None

            recognition_accuracy = result["detection_scores"][0][detected_object]

            # if object is human and accuracy over e.g. 30%
            if (
                result["detection_classes"][0][detected_object] == 1
                and recognition_accuracy > PERSON_RECOGNITION_ACCEPTANCE
            ):
                ymin, xmin, ymax, xmax = tuple(
                    result["detection_boxes"][0][detected_object]
                )

                detected_person_frame = img.reshape(640, 640, 3)[
                    int(ymin * 640) : int(ymax * 640), int(xmin * 640) : int(xmax * 640)
                ].copy()

                resulted_pose_landmarks = pose.process(detected_person_frame)

                tshirt_color = None
                pants_color = None

                # if pose landmarks can be found tshirt and pants color can be determined
                if resulted_pose_landmarks.pose_landmarks:
                    # mp_draw.draw_landmarks(detected_person_frame, resulted_pose_landmarks.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                    landmarks = resulted_pose_landmarks.pose_landmarks.landmark

                    res = get_person_properties(
                        detected_person_frame, landmarks, mp_pose
                    )
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

                if does_exist and person != None:
                    # override person frame if accuracy is better
                    if recognition_accuracy > person.recognition_accuracy:
                        person.person_image = detected_person_frame.copy()
                    # TODO: What happens when I find the person again?
                else:
                    if (
                        len(person_table)
                        < MAX_PERSONS_TRACKED
                        # and tshirt_color
                        # and pants_color
                    ):
                        # TODO: if t and p color cannot be determined: should still be changeable later
                        person = Person(
                            (ymin, xmin, ymax, xmax),
                            tshirt_color,
                            pants_color,
                            detected_person_frame.copy(),
                            recognition_accuracy,
                            time_after_photo,
                        )
                        person_table.append(person)
                        logging.getLogger("recognition_model_daemon").info(
                            "FOUND NEW PERSON"
                        )
                        send_found_person(
                            tshirt_color,
                            pants_color,
                            detected_person_frame.copy(),
                            recognition_accuracy,
                            time_after_photo,
                        )
                    else:
                        least_accuracy_person, table_id = get_least_accuracy_person(
                            person_table
                        )
                        if (
                            least_accuracy_person != None
                            and least_accuracy_person.recognition_accuracy
                            < recognition_accuracy
                            and tshirt_color
                            and pants_color
                        ):
                            del person_table[table_id]
                            person = Person(
                                (ymin, xmin, ymax, xmax),
                                tshirt_color,
                                pants_color,
                                detected_person_frame.copy(),
                                recognition_accuracy,
                                time_after_photo,
                            )
                            person_table.append(person)
                            logging.getLogger("recognition_model_daemon").info(
                                "FOUND NEW PERSON"
                            )

        # TODO: clean up persons from person_table who haven't been seen in a while (add timestamps)
        for person in person_table:
            person.clean_up()
