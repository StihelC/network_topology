import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List
from models import DeviceConfig, BoundaryConfig, ConnectionType

class DeviceDialog(tk.Toplevel):
    """Dialog for adding a new device."""

    def __init__(self, parent: tk.Tk, callback: Callable[[DeviceConfig], None]):
        super().__init__(parent)
        self.callback = callback
        
        self.title("Add Device")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._center_window()

    def _create_widgets(self) -> None:
        """Create dialog widgets."""
        # Name field
        ttk.Label(self, text="Device Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)
        
        # Type field
        ttk.Label(self, text="Device Type:").pack(pady=5)
        device_types = ['router', 'switch', 'firewall', 'server', 'client', 'access_point']
        self.type_var = tk.StringVar(value=device_types[0])
        self.type_combo = ttk.Combobox(
            self,
            textvariable=self.type_var,
            values=device_types,
            state='readonly'
        )
        self.type_combo.pack(pady=5)
        
        # IP Address field
        ttk.Label(self, text="IP Address:").pack(pady=5)
        self.ip_entry = ttk.Entry(self)
        self.ip_entry.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Add",
            command=self._submit
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def _submit(self) -> None:
        """Handle form submission."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Device name is required!")
            return
        
        config = DeviceConfig(
            name=name,
            device_type=self.type_var.get(),
            ip_address=self.ip_entry.get().strip()
        )
        
        self.callback(config)
        self.destroy()

    def _center_window(self) -> None:
        """Center the dialog window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

class BoundaryDialog(tk.Toplevel):
    """Dialog for adding a new boundary."""

    def __init__(self, parent: tk.Tk, callback: Callable[[BoundaryConfig], None]):
        super().__init__(parent)
        self.callback = callback
        
        self.title("Add Network Boundary")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._center_window()

    def _create_widgets(self) -> None:
        """Create dialog widgets."""
        # Name field
        ttk.Label(self, text="Boundary Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)
        
        # Subnet field
        ttk.Label(self, text="Subnet (optional):").pack(pady=5)
        self.subnet_entry = ttk.Entry(self)
        self.subnet_entry.pack(pady=5)
        
        # Description field
        ttk.Label(self, text="Description (optional):").pack(pady=5)
        self.desc_entry = ttk.Entry(self)
        self.desc_entry.pack(pady=5)
        
        # Color field
        ttk.Label(self, text="Color:").pack(pady=5)
        colors = ['#E0E0E0', '#FFE0B2', '#C8E6C9', '#B3E0F2', '#F8BBD0']
        self.color_var = tk.StringVar(value=colors[0])
        self.color_combo = ttk.Combobox(
            self,
            textvariable=self.color_var,
            values=colors,
            state='readonly'
        )
        self.color_combo.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Create",
            command=self._submit
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def _submit(self) -> None:
        """Handle form submission."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Boundary name is required!")
            return
        
        config = BoundaryConfig(
            name=name,
            subnet=self.subnet_entry.get().strip(),
            description=self.desc_entry.get().strip(),
            color=self.color_var.get()
        )
        
        self.callback(config)
        self.destroy()

    def _center_window(self) -> None:
        """Center the dialog window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')