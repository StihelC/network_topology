import tkinter as tk
from tkinter import ttk
from typing import Callable
from models import ConnectionType, Device

class ConnectionDialog(tk.Toplevel):
    """Dialog for creating a connection between devices."""

    def __init__(self, parent: tk.Tk, device1: Device, device2: Device,
                 callback: Callable[[Device, Device, ConnectionType], None]):
        """Initialize the connection dialog.
        
        Args:
            parent: Parent window
            device1: First device to connect
            device2: Second device to connect
            callback: Function to call with connection details
        """
        super().__init__(parent)
        self.device1 = device1
        self.device2 = device2
        self.callback = callback
        
        self.title("Create Connection")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._center_window()

    def _create_widgets(self) -> None:
        """Create dialog widgets."""
        # Header
        header_text = f"Connect {self.device1.config.name} to {self.device2.config.name}"
        ttk.Label(
            self,
            text=header_text,
            font=('Arial', 10, 'bold'),
            wraplength=250
        ).pack(pady=10)
        
        # Connection type selection
        ttk.Label(self, text="Connection Type:").pack(pady=5)
        
        # Create frame for connection types
        conn_frame = ttk.Frame(self)
        conn_frame.pack(pady=10, padx=20)
        
        # Connection type variable
        self.conn_type = tk.StringVar(value=ConnectionType.ETHERNET.value)
        
        # Create radio buttons for each connection type
        for conn_type in ConnectionType:
            ttk.Radiobutton(
                conn_frame,
                text=conn_type.value.title(),
                variable=self.conn_type,
                value=conn_type.value
            ).pack(anchor=tk.W, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Connect",
            command=self._submit
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def _submit(self) -> None:
        """Handle form submission."""
        self.callback(
            self.device1,
            self.device2,
            ConnectionType(self.conn_type.get())
        )
        self.destroy()

    def _center_window(self) -> None:
        """Center the dialog window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')