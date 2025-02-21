import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

@dataclass
class BoundaryConfig:
    """
    BoundaryConfig is a class that represents the configuration of a network boundary.

    Attributes:
        name (str): The name of the boundary.
        subnet (str): The subnet associated with the boundary. Default is an empty string.
        description (str): A description of the boundary. Default is an empty string.
        color (str): The color associated with the boundary, represented as a hex code. Default is light gray ("#E0E0E0").
    """
    name: str
    subnet: str = ""
    description: str = ""
    color: str = "#E0E0E0"  # Default light gray

class NetworkBoundary:
    def __init__(self, canvas, x, y, width, height, config: BoundaryConfig):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.config = config
        self.selected = False
        self.contained_devices = set()
        self.create_boundary()

    def create_boundary(self):
        # Create the boundary rectangle with dashed border
        self.boundary = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill=self.config.color,
            stipple='gray50',  # Creates a semi-transparent effect
            outline='#666666',
            dash=(5, 5),       # Dashed border
            width=2,
            tags=('boundary', 'draggable')
        )

        # Create boundary label at top
        self.name_text = self.canvas.create_text(
            self.x + 10,  # Slight padding from left edge
            self.y + 5,   # Slight padding from top
            text=f"{self.config.name}\n{self.config.subnet}",
            anchor=tk.NW,
            font=('Arial', 10, 'bold'),
            fill='#333333',
            tags=('boundary', 'draggable')
        )

        # Create resize handle
        handle_size = 10
        self.resize_handle = self.canvas.create_rectangle(
            self.x + self.width - handle_size,
            self.y + self.height - handle_size,
            self.x + self.width,
            self.y + self.height,
            fill='white',
            outline='#666666',
            tags=('boundary_resize_handle', 'draggable')
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.boundary, dx, dy)
        self.canvas.move(self.name_text, dx, dy)
        self.canvas.move(self.resize_handle, dx, dy)

    def resize(self, new_width, new_height):
        min_width = 100
        min_height = 100
        self.width = max(new_width, min_width)
        self.height = max(new_height, min_height)
        
        # Update boundary rectangle
        self.canvas.coords(
            self.boundary,
            self.x, self.y,
            self.x + self.width, self.y + self.height
        )
        
        # Update resize handle
        handle_size = 10
        self.canvas.coords(
            self.resize_handle,
            self.x + self.width - handle_size,
            self.y + self.height - handle_size,
            self.x + self.width,
            self.y + self.height
        )

    def contains_point(self, x, y):
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def contains_device(self, device):
        device_x, device_y = device.get_position()
        return self.contains_point(device_x, device_y)

    def highlight(self, state=True):
        color = '#FFE0B2' if state else self.config.color  # Light orange highlight
        self.canvas.itemconfig(self.boundary, fill=color)
        self.selected = state

    def update_contained_devices(self, devices):
        """Update the set of devices contained within this boundary"""
        self.contained_devices.clear()
        for device in devices.values():
            if self.contains_device(device):
                self.contained_devices.add(device)

    def get_info(self):
        """Return a dictionary of boundary information"""
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

class BoundaryDialog(tk.Toplevel):
    def __init__(self, parent, callback, existing_config=None):
        super().__init__(parent)
        self.title("Add Network Boundary")
        self.callback = callback
        
        # Create form fields
        ttk.Label(self, text="Boundary Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)
        
        ttk.Label(self, text="Subnet (optional):").pack(pady=5)
        self.subnet_entry = ttk.Entry(self)
        self.subnet_entry.pack(pady=5)
        
        ttk.Label(self, text="Description (optional):").pack(pady=5)
        self.desc_entry = ttk.Entry(self)
        self.desc_entry.pack(pady=5)
        
        ttk.Label(self, text="Color:").pack(pady=5)
        self.color_var = tk.StringVar(value="#E0E0E0")
        colors = ['#E0E0E0', '#FFE0B2', '#C8E6C9', '#B3E0F2', '#F8BBD0']
        self.color_combo = ttk.Combobox(self, textvariable=self.color_var, values=colors)
        self.color_combo.pack(pady=5)
        
        # Fill in existing values if editing
        if existing_config:
            self.name_entry.insert(0, existing_config.name)
            self.subnet_entry.insert(0, existing_config.subnet)
            self.desc_entry.insert(0, existing_config.description)
            self.color_var.set(existing_config.color)
        
        ttk.Button(self, text="Create Boundary", command=self.submit).pack(pady=20)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()

    def submit(self):
        name = self.name_entry.get().strip()
        if not name:
            tk.messagebox.showerror("Error", "Boundary name is required!")
            return
        
        config = BoundaryConfig(
            name=name,
            subnet=self.subnet_entry.get().strip(),
            description=self.desc_entry.get().strip(),
            color=self.color_var.get()
        )
        
        self.callback(config)
        self.destroy()