from dataclasses import dataclass
from enum import Enum

class ConnectionType(Enum):
    ETHERNET = "ethernet"
    FIBER = "fiber"
    WIRELESS = "wireless"
    VPN = "vpn"
    SERIAL = "serial"
    USB = "usb"

@dataclass
class DeviceConfig:
    name: str
    device_type: str
    ip_address: str = ""
    subnet_mask: str = ""
    location: str = ""

@dataclass
class BoundaryConfig:
    """Configuration for a network boundary.

    Attributes:
        name (str): The name of the boundary.
        subnet (str): The subnet associated with the boundary.
        description (str): A description of the boundary.
        color (str): The color associated with the boundary, represented as a hex code.
    """
    name: str
    subnet: str = ""
    description: str = ""
    color: str = "#E0E0E0"  # Default light gray