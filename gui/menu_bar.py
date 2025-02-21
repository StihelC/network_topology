import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict

class MenuBar:
    """Handles the creation and management of the application menu bar."""

    def __init__(self, root: tk.Tk, callbacks: Dict[str, Callable[[], Any]]):
        """
        Initialize the menu bar.
        
        Args:
            root: The root window
            callbacks: Dictionary of callback functions for menu actions
        """
        self.root = root
        self.callbacks = callbacks
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)
        
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_help_menu()

    def _create_file_menu(self) -> None:
        """Create the File menu."""
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(
            label="New", 
            command=self.callbacks.get('new_topology'),
            accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open", 
            command=self.callbacks.get('load_topology'),
            accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", 
            command=self.callbacks.get('save_topology'),
            accelerator="Ctrl+S"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Export as PNG",
            command=self.callbacks.get('export_topology')
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.root.quit
        )

    def _create_edit_menu(self) -> None:
        """Create the Edit menu."""
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        
        edit_menu.add_command(
            label="Delete Selected",
            command=self.callbacks.get('delete_selected'),
            accelerator="Delete"
        )
        edit_menu.add_command(
            label="Select All",
            command=self.callbacks.get('select_all'),
            accelerator="Ctrl+A"
        )

    def _create_view_menu(self) -> None:
        """Create the View menu."""
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        
        view_menu.add_command(
            label="Zoom In",
            command=self.callbacks.get('zoom_in'),
            accelerator="Ctrl+Plus"
        )
        view_menu.add_command(
            label="Zoom Out",
            command=self.callbacks.get('zoom_out'),
            accelerator="Ctrl+Minus"
        )
        view_menu.add_command(
            label="Reset Zoom",
            command=self.callbacks.get('reset_zoom'),
            accelerator="Ctrl+0"
        )

    def _create_help_menu(self) -> None:
        """Create the Help menu."""
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        
        help_menu.add_command(
            label="About",
            command=self.callbacks.get('show_about')
        )