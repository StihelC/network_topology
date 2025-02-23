from typing import Dict, Tuple, Optional, TYPE_CHECKING
from models.enums import ConnectionType

if TYPE_CHECKING:
    from .device import Device
    import tkinter as tk

class Connection:
    """Represents a connection between two network devices."""

    LINE_STYLES: Dict[ConnectionType, Dict[str, any]] = {
        ConnectionType.ETHERNET: {'dash': None, 'width': 2, 'color': '#2196F3'},
        ConnectionType.FIBER: {'dash': (5,), 'width': 2, 'color': '#FF9800'},
        ConnectionType.WIRELESS: {'dash': (2, 4), 'width': 1, 'color': '#4CAF50'},
        ConnectionType.VPN: {'dash': (8, 4), 'width': 2, 'color': '#9C27B0'},
        ConnectionType.SERIAL: {'dash': (2, 2), 'width': 1, 'color': '#607D8B'},
        ConnectionType.USB: {'dash': (4, 2), 'width': 1, 'color': '#795548'}
    }

    def __init__(self, canvas: 'tk.Canvas', device1: 'Device', 
                 device2: 'Device', connection_type: ConnectionType):
        """Initialize a new connection between two devices."""
        self.canvas = canvas
        self.device1 = device1
        self.device2 = device2
        self.connection_type = connection_type
        self.line: Optional[int] = None
        
        self._create_line()
        
        # Add this connection to both devices
        device1.connections.append(self)
        device2.connections.append(self)

    def _create_line(self) -> None:
        """Create the visual line representing the connection."""
        x1, y1 = self.device1.get_position()
        x2, y2 = self.device2.get_position()
        style = self.LINE_STYLES[self.connection_type]
        
        # Create line with specified style
        self.line = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=style['color'],
            width=style['width'],
            dash=style['dash'],
            tags='connection'  # Add tag for easier management
        )
        
        # Ensure line is below devices but above background
        self.canvas.tag_lower(self.line)
        
        # Update line position to match device centers
        self.update_position()

    def update_position(self) -> None:
        """Update the position of the connection line."""
        if self.line:
            # Get center positions of both devices
            x1, y1 = self.device1.get_position()
            x2, y2 = self.device2.get_position()
            
            # Adjust positions to device centers
            x1 += self.device1.ICON_SIZE // 2
            y1 += self.device1.ICON_SIZE // 2
            x2 += self.device2.ICON_SIZE // 2
            y2 += self.device2.ICON_SIZE // 2
            
            # Update line coordinates
            self.canvas.coords(self.line, x1, y1, x2, y2)
            
            # Ensure line remains visible
            self.canvas.tag_raise(self.line)  # Raise above background
            self.canvas.tag_lower(self.line, 'device')  # Lower below devices

    def delete(self) -> None:
        """Delete the connection and remove it from connected devices."""
        if self.line:
            self.canvas.delete(self.line)
        
        # Remove this connection from both devices
        if self in self.device1.connections:
            self.device1.connections.remove(self)
        if self in self.device2.connections:
            self.device2.connections.remove(self)

    def get_other_device(self, device: 'Device') -> 'Device':
        """Get the device on the other end of the connection."""
        return self.device2 if device == self.device1 else self.device1