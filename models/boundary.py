import tkinter as tk
from typing import Set, Dict, Any, Optional
from models import BoundaryConfig
from models.device import Device

class Boundary:
    """Represents a network boundary/zone that can contain devices."""
    
    MIN_WIDTH = 100
    MIN_HEIGHT = 100
    HANDLE_SIZE = 10

    def __init__(self, canvas: tk.Canvas, x: int, y: int, width: int, height: int, config: BoundaryConfig):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.config = config
        self.contained_devices = []
        self._create_visual_elements()
        
        # Canvas elements
        self.boundary: Optional[int] = None
        self.name_text: Optional[int] = None
        self.resize_handle: Optional[int] = None
        
        self._create_visual_elements()

    def _create_visual_elements(self) -> None:
        """Create the visual elements of the boundary."""
        # Create main boundary rectangle
        self.boundary = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill=self.config.color,
            stipple='gray50',  # Creates a semi-transparent effect
            outline='#666666',
            dash=(5, 5),
            width=2,
            tags=('boundary', 'draggable')
        )

        # Create boundary label
        self.name_text = self.canvas.create_text(
            self.x + 10,
            self.y + 5,
            text=self._get_display_text(),
            anchor=tk.NW,
            font=('Arial', 10, 'bold'),
            fill='#333333',
            tags=('boundary', 'draggable')
        )

        # Create resize handle
        self._create_resize_handle()

    def _create_resize_handle(self) -> None:
        """Create the resize handle in the bottom-right corner."""
        self.resize_handle = self.canvas.create_rectangle(
            self.x + self.width - self.HANDLE_SIZE,
            self.y + self.height - self.HANDLE_SIZE,
            self.x + self.width,
            self.y + self.height,
            fill='white',
            outline='#666666',
            tags=('boundary_resize_handle', 'draggable')
        )

    def _get_display_text(self) -> str:
        """Get the text to display in the boundary label."""
        text = self.config.name
        if self.config.subnet:
            text += f"\n{self.config.subnet}"
        return text

    def move(self, dx: int, dy: int) -> None:
        """Move the boundary by the specified delta."""
        self.x += dx
        self.y += dy
        self.canvas.move(self.boundary, dx, dy)
        self.canvas.move(self.name_text, dx, dy)
        self.canvas.move(self.resize_handle, dx, dy)

    def resize(self, new_width: int, new_height: int) -> None:
        """Resize the boundary to the specified dimensions."""
        self.width = max(new_width, self.MIN_WIDTH)
        self.height = max(new_height, self.MIN_HEIGHT)
        
        # Update boundary rectangle
        self.canvas.coords(
            self.boundary,
            self.x, self.y,
            self.x + self.width, self.y + self.height
        )
        
        # Update resize handle
        self.canvas.coords(
            self.resize_handle,
            self.x + self.width - self.HANDLE_SIZE,
            self.y + self.height - self.HANDLE_SIZE,
            self.x + self.width,
            self.y + self.height
        )

    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point is within the boundary."""
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def contains_device(self, device: Device) -> bool:
        """Check if a device is within the boundary."""
        device_x, device_y = device.get_position()
        return self.contains_point(device_x, device_y)

    def highlight(self, state: bool = True) -> None:
        """Highlight or unhighlight the boundary."""
        color = '#FFE0B2' if state else self.config.color
        self.canvas.itemconfig(self.boundary, fill=color)
        self.selected = state

    def update_contained_devices(self, devices: Dict[str, Device]) -> None:
        """Update the set of devices contained within this boundary."""
        self.contained_devices.clear()
        for device in devices.values():
            if self.contains_device(device):
                self.contained_devices.add(device)

    def get_info(self) -> Dict[str, Any]:
        """Get a dictionary of boundary information for saving."""
        return {
            'name': self.config.name,
            'subnet': self.config.subnet,
            'description': self.config.description,
            'color': self.config.color,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }

    def update_appearance(self) -> None:
        """Update the visual appearance of the boundary."""
        if self.boundary:
            self.canvas.itemconfig(self.boundary, fill=self.config.color)
        if self.name_text:
            self.canvas.itemconfig(self.name_text, text=self._get_display_text())