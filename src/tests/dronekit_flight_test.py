# nohup bash -c "sudo python3 dronekit_flight_test.py"

from dronekit import connect
from dronekit import VehicleMode

import time

vehicle = connect("/dev/ttyACM0", baud=57600, wait_ready=True)
print("Mode: %s" % vehicle.mode.name)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    time.sleep(5)
    
    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    # while True:
    #     print(" Altitude: ", vehicle.location.global_relative_frame.alt)
    #     #Break and return from function just below target altitude.
    #     if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
    #         print("Reached target altitude")
    #         break
    #     time.sleep(1)

arm_and_takeoff(2)

vehicle.mode=VehicleMode('LAND')
while vehicle.mode!='LAND':
	print("Waiting for drone to enter LAND mode")
	time.sleep(1)
print("Vehicle now in LAND mode. Will touch ground shortly.")