from typing import Any, Optional


class GPSData:
    lat: float
    lon: float
    alt: float
    alt_abs: float
    statelites_visible: int
    timestamp: float

    def __init__(self, data: Optional[dict[str, Any]] = None) -> None:
        if data is not None:
            self.from_dict(data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lat": self.lat,
            "lon": self.lon,
            "alt": self.alt,  # relative
            "alt_abs": self.alt_abs,
            "statelites_visible": self.statelites_visible,
            "timestamp": self.timestamp,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        self.lat = data["lat"]
        self.lon = data["lon"]
        self.alt = data["alt"]
        self.alt_abs = data["alt_abs"]
        assert type(data["statelites_visible"]) == int
        self.statelites_visible = data["statelites_visible"]
        self.timestamp = data["timestamp"]
