def emergency_daemon():
    while True:
        if DroneState.vehicle == None:
            print("Vehicle not initialized.")
        if DroneState.emergency:
            DroneState.vehicle.mode = VehicleMode("LAND")
            while DroneState.vehicle.mode != "LAND":
                print("Waiting for drone to enter LAND mode")
                time.sleep(1)
            print("Vehicle now in LAND mode. Will touch ground shortly.")
            sys.exit()
        time.sleep(0.1)
