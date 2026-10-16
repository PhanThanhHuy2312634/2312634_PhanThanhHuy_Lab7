class GPSSignalLostError(Exception):
    """Raised when the device cannot obtain a GPS signal."""


def get_current_location() -> tuple[float, float]:
    """Return the simulated GPS coordinates."""
    return (10.0, 105.0)
