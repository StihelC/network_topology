import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional, Tuple, Callable, Any
from models.device import Device
from models.boundary import Boundary
from models.connection import Connection, ConnectionType

class CanvasPanel:
    """Handles the main drawing area of the application."""

    def __init__(self, parent: ttk.Frame, callbacks: Dict[str, Callable[[], Any]]):
        """Initialize the canvas panel.
        
        Args:
            parent: Parent frame to contain the canvas
            callbacks: Dictionary of callback functions
        """
        self.parent = parent
        self.callbacks = callbacks
        self.devices: Dict[str, Device] = {}
        self.boundaries: Dict[str, Boundary] = {}
        
        # State variables
        self.connecting = False
        self.connection_start: Optional[Device] = None
        self.resizing_boundary: Optional[Boundary] = None
        self.resize_start: Optional[Tuple[int, int]] = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        
        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Create the canvas and scrollbars."""
        # Create canvas frame with scrollbars
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(
            self.frame,
            width=800,
            height=600,
            bg='white',
            scrollregion=(0, 0, 2000, 2000)
        )
        
        # Add scrollbars
        h_scrollbar = ttk.Scrollbar(
            self.frame,
            orient=tk.HORIZONTAL,
            command=self.canvas.xview
        )
        v_scrollbar = ttk.Scrollbar(
            self.frame,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        
        # Configure canvas scroll
        self.canvas.configure(
            xscrollcommand=h_scrollbar.set,
            yscrollcommand=v_scrollbar.set
        )
        
        # Grid layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def _bind_events(self) -> None:
        """Bind canvas events to handlers."""
        # Canvas bindings
        self.canvas.tag_bind('draggable', '<Button-1>', self._drag_start)
        self.canvas.tag_bind('draggable', '<ButtonRelease-1>', self._drag_stop)
        self.canvas.tag_bind('draggable', '<B1-Motion>', self._drag)
        self.canvas.bind('<Button-1>', self._canvas_click)
        
        # Boundary resize handle bindings
        self.canvas.tag_bind('boundary_resize_handle', '<Button-1>', self._resize_start)
        self.canvas.tag_bind('boundary_resize_handle', '<B1-Motion>', self.resizing_boundary)
        self.canvas.tag_bind('boundary_resize_handle', '<ButtonRelease-1>', self._resize_stop)
        
        # Mouse wheel zoom
        self.canvas.bind('<Control-MouseWheel>', self._mouse_wheel_zoom)

    def _drag_start(self, event: tk.Event) -> None:
        """Handle the start of a drag operation."""
        if self.connecting:
            return
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def _drag_stop(self, event: tk.Event) -> None:
        """Handle the end of a drag operation."""
        if self.drag_data["item"]:
            self._update_boundary_devices()
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def _drag(self, event: tk.Event) -> None:
        """Handle drag movement."""
        if self.connecting:
            return
            
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        # Handle device dragging
        for device in self.devices.values():
            if self.drag_data["item"] in (device.icon, device.name_text):
                device.move(dx, dy)
                break
        
        # Handle boundary dragging
        for boundary in self.boundaries.values():
            if self.drag_data["item"] in (boundary.boundary, boundary.name_text):
                boundary.move(dx, dy)
                break
        
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def _canvas_click(self, event: tk.Event) -> None:
        """Handle canvas clicks."""
        if self.connecting:
            self._handle_connection_click(event)
            return

        self._handle_selection_click(event)

    def _handle_connection_click(self, event: tk.Event) -> None:
        """Handle clicks during connection creation."""
        clicked_device = None
        for device in self.devices.values():
            if device.contains(event.x, event.y):
                clicked_device = device
                break
        
        if clicked_device:
            if self.connection_start is None:
                self.connection_start = clicked_device
                clicked_device.highlight(True)
            else:
                if clicked_device != self.connection_start:
                    self.callbacks['create_connection'](
                        self.connection_start,
                        clicked_device
                    )
                
                self.connection_start.highlight(False)
                self.connection_start = None
                self.connecting = False
                self.canvas.config(cursor="")

    def _handle_selection_click(self, event: tk.Event) -> None:
        """Handle selection clicks."""
        # Deselect all
        for device in self.devices.values():
            device.highlight(False)
        for boundary in self.boundaries.values():
            boundary.highlight(False)

        # Check for clicks on devices first
        for device in self.devices.values():
            if device.contains(event.x, event.y):
                device.highlight(True)
                if self.callbacks.get('show_device_properties'):
                    self.callbacks['show_device_properties'](device)
                return

        # Then check boundaries
        for boundary in self.boundaries.values():
            if boundary.contains_point(event.x, event.y):
                boundary.highlight(True)
                if self.callbacks.get('show_boundary_properties'):
                    self.callbacks['show_boundary_properties'](boundary)
                return

    def start_connection_mode(self) -> None:
        """Enter connection creation mode."""
        self.connecting = True
        self.canvas.config(cursor="crosshair")

    def add_device(self, device: Device) -> None:
        """Add a device to the canvas."""
        self.devices[device.config.name] = device
        self._update_boundary_devices()

    def add_boundary(self, boundary: Boundary) -> None:
        """Add a boundary to the canvas."""
        self.boundaries[boundary.config.name] = boundary
        self._update_boundary_devices()

    def _update_boundary_devices(self) -> None:
        """Update device containment for all boundaries."""
        for boundary in self.boundaries.values():
            boundary.update_contained_devices(self.devices)

    def clear(self) -> None:
        """Clear all items from the canvas."""
        self.canvas.delete('all')
        self.devices.clear()
        self.boundaries.clear()
        self.connecting = False
        self.connection_start = None
        self.resizing_boundary = None
        self.resize_start = None
        self.canvas.configure(scrollregion=(0, 0, 2000, 2000))
        self.canvas.config(cursor="")

    def _resize_start(self, event: tk.Event) -> None:
        """Start boundary resizing operation."""
        item = self.canvas.find_closest(event.x, event.y)[0]
        for boundary in self.boundaries.values():
            if item == boundary.resize_handle:
                self.resizing_boundary = boundary
                self.resize_start = (event.x, event.y)
                break

    def resizing_boundary(self, event: tk.Event) -> None:
        """Handle boundary resizing during mouse motion."""
        if not self.resizing_boundary or not self.resize_start:
            return

        # Calculate change in position
        dx = event.x - self.resize_start[0]
        dy = event.y - self.resize_start[1]

        # Update boundary size
        self.resizing_boundary.resize(dx, dy)
        
        # Update start position for next movement
        self.resize_start = (event.x, event.y)
        
        # Update which devices are contained in the boundary
        self._update_boundary_devices()

    def _resize_stop(self, event: tk.Event) -> None:
        """End boundary resizing operation."""
        if self.resizing_boundary:
            self.resizing_boundary = None
            self.resize_start = None

    def _mouse_wheel_zoom(self, event: tk.Event) -> None:
        """Handle mouse wheel zoom events."""
        # Get the current scale
        current_scale = self.canvas.scale("all", 0, 0, 1, 1)
        
        # Define zoom factor (adjust these values to change zoom sensitivity)
        zoom_factor = 1.1 if event.delta > 0 else 0.9
        
        # Get the point to zoom around (mouse position)
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # Apply zoom
        self.canvas.scale("all", x, y, zoom_factor, zoom_factor)
        
        # Update scroll region
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)