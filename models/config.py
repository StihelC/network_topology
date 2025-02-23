from typing import Optional, Dict, Any

class DeviceConfig:
    """Configuration for network devices."""
    
    def __init__(self, name: str, device_type: str):
        self.name = name
        self.device_type = device_type
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization."""
        return {
            'name': self.name,
            'device_type': self.device_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DeviceConfig':
        """Create config from dictionary."""
        return cls(
            name=data['name'],
            device_type=data['device_type']
        )

class BoundaryConfig:
    """Configuration for network boundaries."""
    
    def __init__(self, name: str, boundary_type: str):
        self.name = name
        self.boundary_type = boundary_type
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization."""
        return {
            'name': self.name,
            'boundary_type': self.boundary_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoundaryConfig':
        """Create config from dictionary."""
        return cls(
            name=data['name'],
            boundary_type=data['boundary_type']
        )