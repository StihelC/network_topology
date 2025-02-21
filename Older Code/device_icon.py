import math
import tkinter as tk
from PIL import Image, ImageTk
import os
from models import DeviceConfig

class DeviceIcon:
    ICON_SIZE = 60
    
    def __init__(self, canvas, x, y, config: DeviceConfig):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.config = config
        self.connections = []
        self.selected = False
        self.image_ref = None
        self.create_icon()

    def load_icon(self):
        try:
            # Get the correct path to icons directory
            # Try multiple possible locations
            possible_paths = [
                # Direct path
                os.path.join('icons', f'{self.config.device_type}.png'),
                # From current directory
                os.path.join(os.getcwd(), 'icons', f'{self.config.device_type}.png'),
                # From parent directory
                os.path.join(os.path.dirname(os.getcwd()), 'icons', f'{self.config.device_type}.png'),
            ]

            icon_path = None
            for path in possible_paths:
                print(f"Trying path: {path}")  # Debug print
                if os.path.exists(path):
                    icon_path = path
                    break

            if icon_path:
                print(f"Found icon at: {icon_path}")  # Debug print
                # Load and resize the image
                image = Image.open(icon_path)
                image = image.resize((self.ICON_SIZE, self.ICON_SIZE), Image.Resampling.LANCZOS)
                self.image_ref = ImageTk.PhotoImage(image)
                return True
            else:
                print(f"No icon found for {self.config.device_type}")  # Debug print
                return False

        except Exception as e:
            print(f"Error loading icon: {e}")  # Debug print
            return False

    def create_icon(self):
        if self.load_icon():
            # Create image on canvas
            self.icon = self.canvas.create_image(
                self.x, self.y,
                image=self.image_ref,
                tags=('device', 'draggable')
            )
            print(f"Created image icon for {self.config.device_type}")  # Debug print
        else:
            print(f"Falling back to shape for {self.config.device_type}")  # Debug print
            self._create_fallback_shape()

        # Add device name below the icon
        self.name_text = self.canvas.create_text(
            self.x,
            self.y + self.ICON_SIZE//2 + 10,
            text=self.config.name,
            font=('Arial', 10),
            tags=('device', 'draggable')
        )

    def _create_fallback_shape(self):
        """Create a fallback shape if icon loading fails"""
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

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.icon, dx, dy)
        self.canvas.move(self.name_text, dx, dy)
        for conn in self.connections:
            conn.update_position()

    def get_position(self):
        return (self.x, self.y)

    def contains(self, x, y):
        bbox = self.canvas.bbox(self.icon)
        if not bbox:
            return False
        return (bbox[0] <= x <= bbox[2] and
                bbox[1] <= y <= bbox[3])

    def highlight(self, state=True):
        if state:
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
        else:
            if hasattr(self, 'highlight_circle'):
                self.canvas.delete(self.highlight_circle)
                delattr(self, 'highlight_circle')
                
    def contains(self, x, y):
        """Check if the point (x,y) is within the device icon"""
        bbox = self.canvas.bbox(self.icon)
        if not bbox:
            return False
            
        # Calculate center and radius for hit testing
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        
        # Use the larger of width or height for the radius
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        radius = max(width, height) / 2
        
        # Check if point is within the radius
        distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        is_contained = distance <= radius
        
        if is_contained:
            print(f"Click detected within {self.config.name}")  # Debug print
            
        return is_contained
        
        self.selected = state