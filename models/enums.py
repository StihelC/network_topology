from enum import Enum

class ConnectionType(Enum):
    """Types of connections between network devices."""
    ETHERNET = "ethernet"
    FIBER = "fiber"
    WIRELESS = "wireless"
    VPN = "vpn"
    SERIAL = "serial"
    USB = "usb"