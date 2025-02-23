from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from .config import DeviceConfig, BoundaryConfig
from .enums import ConnectionType
from .device import Device
from .boundary import Boundary
from .connection import Connection

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