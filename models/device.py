import tkinter as tk
from PIL import Image, ImageTk
import os
from typing import List, Tuple, Optional, TYPE_CHECKING
from models import DeviceConfig

if TYPE_CHECKING:
    from models.connection import Connection

class Device:
    """Represents a network device with its visual representation."""
    
    ICON_SIZE = 60
    
    def __init__(self, canvas: tk.Canvas, x: int, y: int, config: DeviceConfig):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.config = config
        self.connections: List['Connection'] = []
        self.selected = False
        self.image_ref: Optional[ImageTk.PhotoImage] = None
        self.icon: Optional[int] = None
        self.name_text: Optional[int] = None
        self.highlight_circle: Optional[int] = None
        self._create_visual_elements()

    def _create_visual_elements(self) -> None:
        """Create the visual elements of the device on the canvas."""
        if self._load_icon():
            # Create image on canvas
            self.icon = self.canvas.create_image(
                self.x, self.y,
                image=self.image_ref,
                tags=('device', 'draggable')
            )
        else:
            self._create_fallback_shape()

        # Add device name below the icon
        self.name_text = self.canvas.create_text(
            self.x,
            self.y + self.ICON_SIZE//2 + 10,
            text=self.config.name,
            font=('Arial', 10),
            tags=('device', 'draggable')
        )

    def _load_icon(self) -> bool:
        """Load the device icon from file."""
        possible_paths = [
            os.path.join('icons', f'{self.config.device_type}.png'),
            os.path.join(os.getcwd(), 'icons', f'{self.config.device_type}.png'),
            os.path.join(os.path.dirname(os.getcwd()), 'icons', f'{self.config.device_type}.png'),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                try:
                    image = Image.open(path)
                    image = image.resize((self.ICON_SIZE, self.ICON_SIZE), Image.Resampling.LANCZOS)
                    self.image_ref = ImageTk.PhotoImage(image)
                    return True
                except Exception:
                    continue

        return False

    def _create_fallback_shape(self) -> None:
        """Create a fallback shape if icon loading fails."""
        size = self.ICON_SIZE // 2
        self.icon = self.canvas.create_rectangle(
            self.x - size,
            self.y - size,
            self.x + size,
            self.y + size,
            fill='gray',
            outline='black',
            width=2,
            tags=('device', 'draggable')
        )

    def move(self, dx: int, dy: int) -> None:
        """Move the device by the specified delta."""
        self.x += dx
        self.y += dy
        self.canvas.move(self.icon, dx, dy)
        self.canvas.move(self.name_text, dx, dy)
        if self.highlight_circle:
            self.canvas.move(self.highlight_circle, dx, dy)
        for conn in self.connections:
            conn.update_position()

    def get_position(self) -> Tuple[int, int]:
        """Get the current position of the device."""
        return (self.x, self.y)

    def contains(self, x: int, y: int) -> bool:
        """Check if the given point is within the device's bounds."""
        bbox = self.canvas.bbox(self.icon)
        if not bbox:
            return False
        
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        radius = max(width, height) / 2
        
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        return distance <= radius

    def highlight(self, state: bool = True) -> None:
        """Highlight or unhighlight the device."""
        if state and not self.highlight_circle:
            bbox = self.canvas.bbox(self.icon)
            if bbox:
                width = bbox[2] - bbox[0]
                height = bbox[3] - bbox[1]
                radius = max(width, height) / 2 + 5
                self.highlight_circle = self.canvas.create_oval(
                    self.x - radius,
                    self.y - radius,
                    self.x + radius,
                    self.y + radius,
                    outline='yellow',
                    width=2,
                    tags=('device', 'draggable')
                )
                self.canvas.tag_lower(self.highlight_circle, self.icon)
        elif not state and self.highlight_circle:
            self.canvas.delete(self.highlight_circle)
            self.highlight_circle = None
        
        self.selected = state

    def delete(self) -> None:
        """Delete the device and its visual elements."""
        if self.icon:
            self.canvas.delete(self.icon)
        if self.name_text:
            self.canvas.delete(self.name_text)
        if self.highlight_circle:
            self.canvas.delete(self.highlight_circle)
        
        # Delete all connections
        for conn in self.connections[:]:  # Use slice copy to avoid modification during iteration
            conn.delete()

    def update_appearance(self) -> None:
        """Update the visual appearance of the device."""
        if self.name_text:
            self.canvas.itemconfig(self.name_text, text=self.config.name)
        # Reload icon if device type changed
        if self.icon:
            self._load_icon()
            if self.image_ref:
                self.canvas.itemconfig(self.icon, image=self.image_ref)