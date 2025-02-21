import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any
from models.device import Device
from models.boundary import Boundary

class PropertiesPanel:
    """Handles the properties panel for displaying and editing device/boundary properties."""

    DEVICE_TYPES = ['router', 'switch', 'firewall', 'server', 'client', 'access_point']
    BOUNDARY_COLORS = ['#E0E0E0', '#FFE0B2', '#C8E6C9', '#B3E0F2', '#F8BBD0']

    def __init__(self, parent: ttk.Frame):
        """Initialize the properties panel."""
        # Create main frame
        self.frame = ttk.LabelFrame(parent, text="Properties")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create scrollable content frame
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.content_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Bind resize events
        self.content_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Initialize variables
        self.current_item = None
        self.property_vars: Dict[str, tk.Variable] = {}
        
        # Show default message
        self._show_default_message()

    def _on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Resize the inner frame to match the canvas."""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _show_default_message(self):
        """Show the default message when no item is selected."""
        self._clear_content()
        ttk.Label(
            self.content_frame,
            text="Select an item to view properties",
            font=('Arial', 10),
            wraplength=200
        ).pack(pady=20)

    def show_device_properties(self, device: Device) -> None:
        """Display properties for a device."""
        self._clear_content()
        self.current_item = device
        
        # Create header
        self._create_header("Device Properties")
        
        # Create property fields
        properties = {
            'name': ('Name:', 'entry', device.config.name),
            'device_type': ('Type:', 'combobox', device.config.device_type, self.DEVICE_TYPES),
            'ip_address': ('IP Address:', 'entry', device.config.ip_address),
        }
        
        self._create_property_fields(properties)
        self._create_apply_button(self._apply_device_changes)

    def show_boundary_properties(self, boundary: Boundary) -> None:
        """Display properties for a boundary."""
        self._clear_content()
        self.current_item = boundary
        
        # Create header
        self._create_header("Boundary Properties")
        
        # Create property fields
        properties = {
            'name': ('Name:', 'entry', boundary.config.name),
            'subnet': ('Subnet:', 'entry', boundary.config.subnet),
            'color': ('Color:', 'combobox', boundary.config.color, self.BOUNDARY_COLORS),
        }
        
        self._create_property_fields(properties)
        self._create_apply_button(self._apply_boundary_changes)
        
        # Show contained devices
        self._show_contained_devices(boundary)

    def _clear_content(self) -> None:
        """Clear all widgets from the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.property_vars.clear()

    def _create_header(self, text: str) -> None:
        """Create a header with the given text."""
        ttk.Label(
            self.content_frame,
            text=text,
            font=('Arial', 12, 'bold')
        ).pack(pady=10)

    def _create_property_fields(self, properties: Dict[str, tuple]) -> None:
        """Create property fields based on the provided properties dictionary."""
        for prop_name, (label, field_type, value, *args) in properties.items():
            frame = ttk.Frame(self.content_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Create label
            ttk.Label(frame, text=label).pack(side=tk.LEFT)
            
            # Create input field
            if field_type == 'entry':
                var = tk.StringVar(value=value)
                ttk.Entry(frame, textvariable=var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            elif field_type == 'combobox':
                var = tk.StringVar(value=value)
                ttk.Combobox(
                    frame,
                    textvariable=var,
                    values=args[0],
                    state='readonly'
                ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            
            self.property_vars[prop_name] = var

    def _create_apply_button(self, command) -> None:
        """Create an apply button with the given command."""
        ttk.Button(
            self.content_frame,
            text="Apply Changes",
            command=command
        ).pack(pady=10)

    def _apply_device_changes(self) -> None:
        """Apply changes to the current device."""
        if isinstance(self.current_item, Device):
            self.current_item.config.name = self.property_vars['name'].get()
            self.current_item.config.device_type = self.property_vars['device_type'].get()
            self.current_item.config.ip_address = self.property_vars['ip_address'].get()
            self.current_item.update_appearance()

    def _apply_boundary_changes(self) -> None:
        """Apply changes to the current boundary."""
        if isinstance(self.current_item, Boundary):
            self.current_item.config.name = self.property_vars['name'].get()
            self.current_item.config.subnet = self.property_vars['subnet'].get()
            self.current_item.config.color = self.property_vars['color'].get()
            self.current_item.update_appearance()

    def _show_contained_devices(self, boundary: Boundary) -> None:
        """Display the list of devices contained within a boundary."""
        ttk.Label(
            self.content_frame,
            text="Contained Devices",
            font=('Arial', 10, 'bold')
        ).pack(pady=(15, 5))
        
        # Create scrolled text widget for devices
        text_frame = ttk.Frame(self.content_frame)
        text_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        text_widget = tk.Text(
            text_frame,
            height=5,
            width=30,
            wrap=tk.WORD
        )
        text_scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add devices to text widget
        for device in boundary.contained_devices:
            text_widget.insert(tk.END, f"{device.config.name}\n")
        
        text_widget.configure(state='disabled')