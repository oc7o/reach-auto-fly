from dronekit import LocationGlobal, LocationGlobalRelative

from reach.exceptions import NoVehicleConnectionException
from reach.thread_management import drone_state


def drone_is_initialized() -> bool:
    if drone_state.vehicle is None:
        # loggers["flight_controller_daemon"].warning(
        #     "Connection to flight controller not initialized, unable to perform actions on vehicle"
        # )
        return False
    return True


def get_gps() -> dict:
    if drone_state.vehicle is None:
        raise NoVehicleConnectionException()

    global_location: LocationGlobal = drone_state.vehicle.location.global_frame
    global_location_ra: LocationGlobalRelative = (
        drone_state.vehicle.location.global_relative_frame
    )
    statelites_visible: int = drone_state.vehicle.gps_0.satellites_visible

    # absolute_altitude = global_location.alt
    # relative_altitude = global_location_ra.alt

    return {
        "lat": global_location.lat,
        "lon": global_location.lon,
        "alt": global_location_ra.alt,  # relative
        "alt_abs": global_location.alt,
        "statelites_visible": statelites_visible,
    }
