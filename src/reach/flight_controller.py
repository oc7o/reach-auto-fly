import time

from dronekit import LocationGlobalRelative, VehicleMode

from reach.config import MAXIMUM_WAIT_COUNT


def arm_and_takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    wait_count = 0
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        if wait_count >= MAXIMUM_WAIT_COUNT:
            print("[ERROR] Could not initialise!")
            return
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
        wait_count += 1

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    wait_count = 0
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        if wait_count >= MAXIMUM_WAIT_COUNT:
            print("[ERROR] Could not arm!")
            return
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    # while True:
    #     print(" Altitude: ", vehicle.location.global_relative_frame.alt)
    #     #Break and return from function just below target altitude.
    #     if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
    #         print("Reached target altitude")
    #         break
    #     time.sleep(1)


def land(vehicle):
    vehicle.mode = VehicleMode("LAND")
    while vehicle.mode != "LAND":
        print("Waiting for drone to enter LAND mode")
        time.sleep(1)
    print("Vehicle now in LAND mode. Will touch ground shortly.")


def hold_postion(vehicle):
    latitude = vehicle.location.global_relative_frame.lat
    longitude = vehicle.location.global_relative_frame.lon
    altitude = None

    a_location = LocationGlobalRelative(latitude, longitude, altitude)
