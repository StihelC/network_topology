import json
import os
from typing import Dict, Any, Optional
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from models import DeviceConfig, BoundaryConfig, ConnectionType, Boundary, Device

class FileHandler:
    """Handles file operations for the topology designer."""

    @staticmethod
    def save_topology(canvas: tk.Canvas, devices: Dict[str, 'Device'],
                     boundaries: Dict[str, 'Boundary'], filename: str) -> bool:
        """Save the current topology to a JSON file.
        
        Args:
            canvas: The canvas containing the topology
            devices: Dictionary of devices
            boundaries: Dictionary of boundaries
            filename: Path to save the file
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            topology = {
                'devices': [],
                'connections': [],
                'boundaries': []
            }
            
            # Save devices
            for device in devices.values():
                topology['devices'].append({
                    'name': device.config.name,
                    'type': device.config.device_type,
                    'ip': device.config.ip_address,
                    'x': device.x,
                    'y': device.y
                })
            
            # Save connections (avoid duplicates)
            seen_connections = set()
            for device in devices.values():
                for conn in device.connections:
                    # Create unique identifier for connection
                    conn_pair = tuple(sorted([
                        conn.device1.config.name,
                        conn.device2.config.name
                    ]))
                    if conn_pair not in seen_connections:
                        topology['connections'].append({
                            'device1': conn.device1.config.name,
                            'device2': conn.device2.config.name,
                            'type': conn.connection_type.value
                        })
                        seen_connections.add(conn_pair)
            
            # Save boundaries
            for boundary in boundaries.values():
                topology['boundaries'].append({
                    'name': boundary.config.name,
                    'subnet': boundary.config.subnet,
                    'description': boundary.config.description,
                    'color': boundary.config.color,
                    'x': boundary.x,
                    'y': boundary.y,
                    'width': boundary.width,
                    'height': boundary.height
                })
            
            # Save to file with pretty printing
            with open(filename, 'w') as f:
                json.dump(topology, f, indent=2)
            
            return True
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save topology: {str(e)}")
            return False

    @staticmethod
    def load_topology(filename: str) -> Optional[Dict[str, Any]]:
        """Load a topology from a JSON file.
        
        Args:
            filename: Path to the file to load
            
        Returns:
            Optional[Dict[str, Any]]: The loaded topology data or None if loading failed
        """
        try:
            with open(filename, 'r') as f:
                topology = json.load(f)
            
            # Validate topology structure
            if not all(key in topology for key in ['devices', 'connections', 'boundaries']):
                raise ValueError("Invalid topology file format")
            
            return topology
            
        except json.JSONDecodeError:
            messagebox.showerror("Load Error", "Invalid JSON file format")
            return None
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load topology: {str(e)}")
            return None

    @staticmethod
    def export_topology(canvas: tk.Canvas, filename: str) -> bool:
        """Export the topology as a PNG image.
        
        Args:
            canvas: The canvas containing the topology
            filename: Path to save the image
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            # Get canvas bounds
            bbox = canvas.bbox("all")
            if not bbox:
                messagebox.showwarning("Warning", "Nothing to export - canvas is empty!")
                return False

            # Add padding
            padding = 20
            x1, y1, x2, y2 = bbox
            bbox = (x1 - padding, y1 - padding, x2 + padding, y2 + padding)

            # Generate PostScript file
            ps_path = f"{filename}.ps"
            canvas.postscript(
                file=ps_path,
                colormode='color',
                pagewidth=x2-x1+2*padding,
                pageheight=y2-y1+2*padding,
                bbox=bbox
            )

            # Convert to PNG
            with Image.open(ps_path) as img:
                # Convert to RGB mode to ensure proper color handling
                img = img.convert('RGB')
                img.save(filename, 'PNG')

            # Clean up temporary PostScript file
            os.remove(ps_path)
            
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export topology: {str(e)}\n\n"
                "Make sure you have Pillow installed."
            )
            # Clean up any partial files
            for f in [ps_path, filename]:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass
            return False

    @staticmethod
    def validate_device_position(x: int, y: int, canvas: tk.Canvas) -> tuple[int, int]:
        """Validate and adjust device position to ensure it's within canvas bounds.
        
        Args:
            x: Proposed x coordinate
            y: Proposed y coordinate
            canvas: The canvas to check bounds against
            
        Returns:
            tuple[int, int]: Adjusted (x, y) coordinates
        """
        # Get canvas dimensions
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # Add padding
        padding = 30
        
        # Adjust coordinates if needed
        x = max(padding, min(x, canvas_width - padding))
        y = max(padding, min(y, canvas_height - padding))
        
        return (x, y)