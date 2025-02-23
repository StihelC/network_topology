from typing import Dict, Any
import tkinter as tk
from tkinter import Tk, Frame, Menu, ttk, messagebox, filedialog, BOTH, LEFT, TOP, X, Y
from typing import Optional, Callable

from .menu_bar import MenuBar
from .toolbar import Toolbar
from .canvas_panel import CanvasPanel
from .properties_panel import PropertiesPanel

from models.device import Device
from models.boundary import Boundary
from models.connection import Connection
from models.enums import ConnectionType
from models.config import DeviceConfig, BoundaryConfig
import json

class DeviceConfig:
    def __init__(self, name: str, device_type: str):
        self.name = name
        self.device_type = device_type

class BoundaryConfig:
    def __init__(self, name: str, boundary_type: str):
        self.name = name
        self.boundary_type = boundary_type

class NetworkTopologyGUI:
    """Main application window class."""

    def __init__(self, root: Tk):
        self.root = root
        self._create_widgets()
        self._create_menu()

    def _create_callbacks(self) -> Dict[str, Any]:
        """Create callback registry for GUI components."""
        return {
            # File operations
            'new_topology': self._new_topology,
            'load_topology': self._load_topology,
            'save_topology': self._save_topology,
            'export_topology': self._export_topology,
            
            # Edit operations
            'delete_selected': self._delete_selected,
            'select_all': self._select_all,
            
            # View operations
            'zoom_in': self._zoom_in,
            'zoom_out': self._zoom_out,
            'reset_zoom': self._reset_zoom,
            
            # Device operations
            'add_device': self._show_add_device_dialog,
            'bulk_add': self._show_bulk_add_dialog,
            'show_device_properties': self._show_device_properties,
            
            # Boundary operations
            'add_boundary': self._show_add_boundary_dialog,
            'show_boundary_properties': self._show_boundary_properties,
            
            # Connection operations
            'start_connection': self._start_connection_mode,
            'create_connection': self._create_connection,
            
            # Help operations
            'show_about': self._show_about_dialog
        }

    def _create_widgets(self) -> None:
        """Create and arrange the main GUI widgets."""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Initialize callback registry
        self.callbacks = self._create_callbacks()
        
        # Create GUI components
        self._create_components()
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()

    def _create_menu(self) -> None:
        """Create and initialize the menu bar."""
        self.menu_bar = MenuBar(self.root, self.callbacks)

    def _create_components(self) -> None:
        """Create and initialize all GUI components."""
        # Create toolbar
        self.toolbar = Toolbar(self.main_frame, self.callbacks)
        
        # Create main content pane
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas panel
        canvas_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(canvas_frame, weight=3)
        self.canvas_panel = CanvasPanel(canvas_frame, self.callbacks)
        
        # Create properties panel
        properties_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(properties_frame, weight=1)
        self.properties_panel = PropertiesPanel(properties_frame)

    def _bind_shortcuts(self) -> None:
        """Bind keyboard shortcuts to actions."""
        self.root.bind('<Control-n>', self.callbacks['new_topology'])
        self.root.bind('<Control-o>', self.callbacks['load_topology'])
        self.root.bind('<Control-s>', self.callbacks['save_topology'])
        self.root.bind('<Delete>', self.callbacks['delete_selected'])
        self.root.bind('<Control-a>', self.callbacks['select_all'])
        self.root.bind('<Control-plus>', self.callbacks['zoom_in'])
        self.root.bind('<Control-minus>', self.callbacks['zoom_out'])
        self.root.bind('<Control-0>', self.callbacks['reset_zoom'])

    # File operations
    def _new_topology(self, event=None) -> None:
        """Create a new empty topology."""
        if self.canvas_panel.devices or self.canvas_panel.boundaries:
            if not messagebox.askyesno("New Topology", 
                "Are you sure you want to create a new topology? All unsaved changes will be lost."):
                return
        
        self.canvas_panel.clear()
        self.properties_panel._show_default_message()

    def _load_topology(self, event=None) -> None:
        """Load a topology from a file."""
        # Implementation will be added with file handling utilities
        pass

    def _save_topology(self, event=None) -> None:
        """Save the current topology to a file."""
        # Implementation will be added with file handling utilities
        def _save_topology_as(event=None) -> None:
            """Save the current topology to a new file."""
            filename = filedialog.asksaveasfilename(
                defaultextension=".ntd",
                filetypes=[("Network Topology Designer files", "*.ntd"), ("All files", "*.*")]
            )
            
            if not filename:
                return

            topology_data = {
                'devices': [device.to_dict() for device in self.canvas_panel.devices],
                'boundaries': [boundary.to_dict() for boundary in self.canvas_panel.boundaries],
                'connections': [connection.to_dict() for connection in self.canvas_panel.connections]
            }

            try:
                with open(filename, 'w') as f:
                    json.dump(topology_data, f, indent=4)
                messagebox.showinfo("Success", "Topology saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save topology: {str(e)}")
        _save_topology_as()

    def _export_topology(self, event=None) -> None:
        """Export the topology as an image."""
        # Implementation will be added with export utilities
        pass

    # Edit operations
    def _delete_selected(self, event=None) -> None:
        """Delete the currently selected items."""
        self.canvas_panel.delete_selected()
        self.properties_panel._show_default_message()

    def _select_all(self, event=None) -> None:
        """Select all items in the topology."""
        self.canvas_panel.select_all()

    # View operations
    def _zoom_in(self, event=None) -> None:
        """Increase the zoom level."""
        self.canvas_panel.zoom_in()
        self._update_zoom_display()

    def _zoom_out(self, event=None) -> None:
        """Decrease the zoom level."""
        self.canvas_panel.zoom_out()
        self._update_zoom_display()

    def _reset_zoom(self, event=None) -> None:
        """Reset zoom to 100%."""
        self.canvas_panel.reset_zoom()
        self._update_zoom_display()

    def _update_zoom_display(self) -> None:
        """Update the zoom level display in the toolbar."""
        zoom_level = self.canvas_panel.get_zoom_level()
        self.toolbar.update_zoom_label(zoom_level)

    # Device operations
    def _show_add_device_dialog(self) -> None:
        """Show dialog for adding a new device."""
        from .dialogs import DeviceDialog
        def on_device_added(config):
            from models.device import Device
            # Pass the canvas object from canvas_panel instead of 100.
            device = Device(self.canvas_panel.canvas, 100, 100, config)
            self.canvas_panel.add_device(device)

        dialog = DeviceDialog(self.root, on_device_added)
        self.root.wait_window(dialog)


    def _show_bulk_add_dialog(self) -> None:
        """Show dialog for bulk adding devices."""
        from tkinter import messagebox
        # For now, simply show a message that bulk add is not implemented.
        messagebox.showinfo("Bulk Add", "Bulk add functionality is not implemented yet.")

    def _show_device_properties(self, device: Device) -> None:
        """Show properties for the selected device."""
        self.properties_panel.show_device_properties(device)

    # Boundary operations
    def _show_add_boundary_dialog(self) -> None:
        """Show dialog for adding a new boundary."""
        from .dialogs import BoundaryDialog
        def on_boundary_added(config):
            self.on_boundary_added(config)
        dialog = BoundaryDialog(self.root, on_boundary_added)
        self.root.wait_window(dialog)

    def on_boundary_added(self, config: BoundaryConfig) -> None:
        """Handle boundary creation."""
        x = 100
        y = 100
        width = 200
        height = 150
        
        boundary = Boundary(
            canvas=self.canvas_panel.canvas,
            x=x,
            y=y,
            width=width,
            height=height,
            config=config
        )
        self.canvas_panel.add_boundary(boundary)

    def _show_boundary_properties(self, boundary: Boundary) -> None:
        """Show properties for the selected boundary."""
        self.properties_panel.show_boundary_properties(boundary)

    # Connection operations
    def _start_connection_mode(self) -> None:
        """Enter connection creation mode."""
        self.canvas_panel.start_connection_mode()

    def _create_connection(self, device1: Device, device2: Device) -> None:
        """Create a connection between two devices."""
        # Implementation will be added with connection dialog
        pass

    # Help operations
    def _show_about_dialog(self) -> None:
        """Show the about dialog."""
        messagebox.showinfo(
            "About Network Topology Designer",
            "Network Topology Designer v1.0\n\n"
            "A tool for designing and visualizing network topologies.\n\n"
            "Created with Python and Tkinter."
        )
