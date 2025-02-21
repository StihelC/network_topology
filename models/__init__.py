from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

class ConnectionType(Enum):
    ETHERNET = "ethernet"
    FIBER = "fiber"
    WIRELESS = "wireless"
    VPN = "vpn"
    SERIAL = "serial"
    USB = "usb"

@dataclass
class DeviceConfig:
    """Configuration for a network device."""
    name: str
    device_type: str
    ip_address: str = ""
    subnet_mask: str = ""
    location: str = ""

@dataclass
class BoundaryConfig:
    """Configuration for a network boundary/zone."""
    name: str
    subnet: str = ""
    description: str = ""
    color: str = "#E0E0E0"  # Default light gray