class NoVehicleConnectionException(Exception):
    def __str__(self):
        return "No vehicle connection"


class NoMQTTConnectionException(Exception):
    def __str__(self):
        return "No mqtt connection"
