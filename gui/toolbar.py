import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict

class Toolbar:
    """Handles the creation and management of the application toolbar."""

    def __init__(self, parent: ttk.Frame, callbacks: Dict[str, Callable[[], Any]]):
        """
        Initialize the toolbar.
        
        Args:
            parent: Parent frame to contain the toolbar
            callbacks: Dictionary of callback functions for toolbar actions
        """
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        self.callbacks = callbacks
        
        self._create_main_buttons()
        self._create_zoom_controls()

    def _create_main_buttons(self) -> None:
        """Create the main toolbar buttons."""
        buttons = [
            ("Add Device", 'add_device'),
            ("Bulk Add", 'bulk_add'),
            ("Add Boundary", 'add_boundary'),
            ("Connect Devices", 'start_connection'),
            ("Delete Selected", 'delete_selected'),
            ("Save", 'save_topology'),
            ("Load", 'load_topology')
        ]
        
        for text, callback_key in buttons:
            ttk.Button(
                self.frame,
                text=text,
                command=self.callbacks.get(callback_key)
            ).pack(side=tk.LEFT, padx=5)

    def _create_zoom_controls(self) -> None:
        """Create the zoom control section of the toolbar."""
        zoom_frame = ttk.Frame(self.frame)
        zoom_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT)
        
        ttk.Button(
            zoom_frame,
            text="-",
            width=2,
            command=self.callbacks.get('zoom_out')
        ).pack(side=tk.LEFT, padx=2)
        
        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            zoom_frame,
            text="+",
            width=2,
            command=self.callbacks.get('zoom_in')
        ).pack(side=tk.LEFT, padx=2)

    def update_zoom_label(self, percentage: int) -> None:
        """Update the zoom percentage display.
        
        Args:
            percentage: The zoom percentage to display
        """
        self.zoom_label.config(text=f"{percentage}%")