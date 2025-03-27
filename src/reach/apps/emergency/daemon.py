def emergency_daemon():
    while True:
        if drone_state.vehicle == None:
            print("Vehicle not initialized.")
        if drone_state.emergency:
            drone_state.vehicle.mode = VehicleMode("LAND")
            while drone_state.vehicle.mode != "LAND":
                print("Waiting for drone to enter LAND mode")
                time.sleep(1)
            print("Vehicle now in LAND mode. Will touch ground shortly.")
            sys.exit()
        time.sleep(0.1)
