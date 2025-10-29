class PortRange:
    """A range of network ports."""
    low: int
    high: int

    def __init__(self, low: int, high: int):
        """Initializes a PortRange with the given low and high values."""
        self.low = low
        self.high = high

    @staticmethod
    def default():
        """Returns the default port range (1-1000)"""
        return PortRange(1, 1000)

    @staticmethod
    def max():
        """Returns the maximum port range (1-65535)"""
        return PortRange(1, 65535)

    @staticmethod
    def parse(range_str: str):
        """Parses a port range string and returns a PortRange object."""
        if "-" in range_str:
            parts = range_str.split("-")
            low = int(parts[0]) if parts[0] else 1
            high = int(parts[1]) if parts[1] else 65535
            return PortRange(low, high)
        else:
            raise ValueError("Invalid port range format")
