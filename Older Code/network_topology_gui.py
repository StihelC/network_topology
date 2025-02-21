import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from device_icon import DeviceIcon
from bulk_device_dialog import BulkDeviceDialog
from models import DeviceConfig, ConnectionType, BoundaryConfig
from connection import Connection
from network_boundary import NetworkBoundary, BoundaryDialog


class NetworkTopologyGUI:
    """
    A GUI application for designing network topologies.
    Attributes:
        root (tk.Tk): The root window of the application.
        main_frame (ttk.Frame): The main frame of the application.
        devices (dict): A dictionary to store device objects.
        boundaries (dict): A dictionary to store boundary objects.
        drag_data (dict): A dictionary to store drag event data.
        connecting (bool): A flag to indicate if devices are being connected.
        connection_start (tuple): The starting point of a connection.
        resizing_boundary (NetworkBoundary): The boundary currently being resized.
        resize_start (tuple): The starting point of a resize event.
    Methods:
        __init__(root): Initializes the GUI application.
        create_menu(): Creates the menu bar.
        create_toolbar(): Creates the toolbar with buttons.
        create_main_panel(): Creates the main panel with canvas and side panel.
        create_properties_panel(): Creates the properties panel in the side panel.
        show_device_properties(device): Displays the properties of a selected device.
        show_boundary_properties(boundary): Displays the properties of a selected boundary.
        bind_events(): Binds events to the canvas and other widgets.
        drag_start(event): Handles the start of a drag event.
        drag_stop(event): Handles the end of a drag event.
        drag(event): Handles the dragging of items on the canvas.
        add_device_dialog(): Opens a dialog to add a new device.
        show_bulk_add_dialog(): Opens a dialog to add multiple devices.
        add_boundary_dialog(): Opens a dialog to add a new boundary.
        resize_start(event): Handles the start of a boundary resize event.
        resize_boundary(event): Handles the resizing of a boundary.
        resize_stop(event): Handles the end of a boundary resize event.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Network Topology Designer")
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main panel with canvas and side panel
        self.create_main_panel()
        
        # Initialize storages
        self.devices = {}
        self.boundaries = {}
        
        # Bind events
        self.bind_events()
        
        # Initialize states
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.connecting = False
        self.connection_start = None
        self.resizing_boundary = None
        self.resize_start = None

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_topology)
        file_menu.add_command(label="Open", command=self.load_topology)
        file_menu.add_command(label="Save", command=self.save_topology)
        file_menu.add_separator()
        file_menu.add_command(label="Export as PNG", command=self.export_topology)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Delete Selected", command=self.delete_selected)
        edit_menu.add_command(label="Select All", command=self.select_all)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_toolbar(self):
        """Create the toolbar with all button options"""
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Create all toolbar buttons
        buttons = [
            ("Add Device", self.add_device_dialog),
            ("Bulk Add", self.show_bulk_add_dialog),
            ("Add Boundary", self.add_boundary_dialog),
            ("Connect Devices", self.start_connection_mode),
            ("Delete Selected", self.delete_selected),
            ("Save", self.save_topology),
            ("Load", self.load_topology)
        ]
        
        # Add all buttons to toolbar
        for text, command in buttons:
            ttk.Button(toolbar, text=text, command=command).pack(side=tk.LEFT, padx=5)
        
        # Add zoom controls
        zoom_frame = ttk.Frame(toolbar)
        zoom_frame.pack(side=tk.RIGHT, padx=5)
        ttk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT)
        ttk.Button(zoom_frame, text="-", width=2, command=self.zoom_out).pack(side=tk.LEFT, padx=2)
        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="+", width=2, command=self.zoom_in).pack(side=tk.LEFT, padx=2)

    def create_main_panel(self):
        # Create main panel with canvas and side panel
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas frame with scrollbars
        canvas_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(canvas_frame, weight=3)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(
            canvas_frame,
            width=800,
            height=600,
            bg='white',
            scrollregion=(0, 0, 2000, 2000)  # Initial scroll region
        )
        
        # Add scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        # Configure canvas scroll
        self.canvas.configure(
            xscrollcommand=h_scrollbar.set,
            yscrollcommand=v_scrollbar.set
        )
        
        # Grid layout for canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Create side panel
        self.side_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(self.side_panel, weight=1)
        
        # Create properties panel in side panel 
        self.create_properties_panel()

        def create_properties_panel(self):
            # Properties Panel
            properties_frame = ttk.LabelFrame(self.side_panel, text="Properties")
            properties_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Properties content
            self.properties_content = ttk.Frame(properties_frame)
            self.properties_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Default message
            self.default_properties_label = ttk.Label(
                self.properties_content,
                text="Select an item to view properties"
            )
            self.default_properties_label.pack(pady=20)

    def show_device_properties(self, device):
        # Clear current properties
        for widget in self.properties_content.winfo_children():
            widget.destroy()
        
        # Create device properties form
        ttk.Label(self.properties_content, text="Device Properties", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Name
        name_frame = ttk.Frame(self.properties_content)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        name_var = tk.StringVar(value=device.config.name)
        name_entry = ttk.Entry(name_frame, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, padx=5)
        
        # Type
        type_frame = ttk.Frame(self.properties_content)
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT)
        type_var = tk.StringVar(value=device.config.device_type)
        type_combo = ttk.Combobox(
            type_frame,
            textvariable=type_var,
            values=['router', 'switch', 'firewall', 'server', 'client', 'access_point'],
            state='readonly'
        )
        type_combo.pack(side=tk.LEFT, padx=5)
        
        # IP Address
        ip_frame = ttk.Frame(self.properties_content)
        ip_frame.pack(fill=tk.X, pady=5)
        ttk.Label(ip_frame, text="IP:").pack(side=tk.LEFT)
        ip_var = tk.StringVar(value=device.config.ip_address)
        ip_entry = ttk.Entry(ip_frame, textvariable=ip_var)
        ip_entry.pack(side=tk.LEFT, padx=5)
        
        # Apply button
        def apply_changes():
            device.config.name = name_var.get()
            device.config.device_type = type_var.get()
            device.config.ip_address = ip_var.get()
            # Update visual representation
            device.update_appearance()
            
        ttk.Button(self.properties_content, text="Apply Changes", command=apply_changes).pack(pady=10)

    def show_boundary_properties(self, boundary):
        # Clear current properties
        for widget in self.properties_content.winfo_children():
            widget.destroy()
        
        # Create boundary properties form
        ttk.Label(self.properties_content, text="Boundary Properties", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Name
        name_frame = ttk.Frame(self.properties_content)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        name_var = tk.StringVar(value=boundary.config.name)
        name_entry = ttk.Entry(name_frame, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, padx=5)
        
        # Subnet
        subnet_frame = ttk.Frame(self.properties_content)
        subnet_frame.pack(fill=tk.X, pady=5)
        ttk.Label(subnet_frame, text="Subnet:").pack(side=tk.LEFT)
        subnet_var = tk.StringVar(value=boundary.config.subnet)
        subnet_entry = ttk.Entry(subnet_frame, textvariable=subnet_var)
        subnet_entry.pack(side=tk.LEFT, padx=5)
        
        # Color
        color_frame = ttk.Frame(self.properties_content)
        color_frame.pack(fill=tk.X, pady=5)
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT)
        color_var = tk.StringVar(value=boundary.config.color)
        color_combo = ttk.Combobox(
            color_frame,
            textvariable=color_var,
            values=['#E0E0E0', '#FFE0B2', '#C8E6C9', '#B3E0F2', '#F8BBD0'],
            state='readonly'
        )
        color_combo.pack(side=tk.LEFT, padx=5)
        
        # Apply button
        def apply_changes():
            boundary.config.name = name_var.get()
            boundary.config.subnet = subnet_var.get()
            boundary.config.color = color_var.get()
            # Update visual representation
            boundary.update_appearance()
            
        ttk.Button(self.properties_content, text="Apply Changes", command=apply_changes).pack(pady=10)
        
        # Show contained devices
        ttk.Label(self.properties_content, text="Contained Devices:", font=('Arial', 10, 'bold')).pack(pady=10)
        devices_text = tk.Text(self.properties_content, height=5, width=30)
        devices_text.pack(pady=5)
        for device in boundary.contained_devices:
            devices_text.insert(tk.END, f"{device.config.name}\n")
        devices_text.configure(state='disabled')

    def bind_events(self):
        # Canvas bindings
        self.canvas.tag_bind('draggable', '<Button-1>', self.drag_start)
        self.canvas.tag_bind('draggable', '<ButtonRelease-1>', self.drag_stop)
        self.canvas.tag_bind('draggable', '<B1-Motion>', self.drag)
        self.canvas.bind('<Button-1>', self.canvas_click)
        
        # Boundary resize handle bindings
        self.canvas.tag_bind('boundary_resize_handle', '<Button-1>', self.resize_start)
        self.canvas.tag_bind('boundary_resize_handle', '<B1-Motion>', self.resize_boundary)
        self.canvas.tag_bind('boundary_resize_handle', '<ButtonRelease-1>', self.resize_stop)
        
        # Mouse wheel zoom
        self.canvas.bind('<Control-MouseWheel>', self.mouse_wheel_zoom)
        
        # Key bindings
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        self.root.bind('<Control-s>', lambda e: self.save_topology())
        self.root.bind('<Control-o>', lambda e: self.load_topology())
        self.root.bind('<Control-n>', lambda e: self.new_topology())

    def drag_start(self, event):
        if self.connecting:
            return
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag_stop(self, event):
        if self.drag_data["item"]:
            # Update boundary containment after drag
            self.update_boundary_devices()
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def drag(self, event):
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

    def add_device_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Device")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Device Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Device Type:").pack(pady=5)
        device_types = ['router', 'switch', 'firewall', 'server', 'client', 'access_point']
        type_var = tk.StringVar(value=device_types[0])
        type_combo = ttk.Combobox(dialog, textvariable=type_var, values=device_types, state='readonly')
        type_combo.pack(pady=5)
        
        ttk.Label(dialog, text="IP Address:").pack(pady=5)
        ip_entry = ttk.Entry(dialog)
        ip_entry.pack(pady=5)
        
        def submit():
            name = name_entry.get().strip()
            device_type = type_var.get()
            ip = ip_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Device name is required!")
                return
            
            config = DeviceConfig(
                name=name,
                device_type=device_type,
                ip_address=ip
            )
            
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            
            device = DeviceIcon(self.canvas, x, y, config)
            self.devices[config.name] = device
            
            dialog.destroy()
        
        ttk.Button(dialog, text="Add Device", command=submit).pack(pady=20)

    def show_bulk_add_dialog(self):
        """Show the bulk add dialog window"""
        def add_devices(devices):
            try:
                # Calculate grid layout
                devices_per_row = 3
                spacing = 150
                start_x = 100
                start_y = 100
                
                for i, device_config in enumerate(devices):
                    # Calculate position
                    row = i // devices_per_row
                    col = i % devices_per_row
                    
                    x = start_x + (col * spacing)
                    y = start_y + (row * spacing)
                    
                    # Create the device
                    device = DeviceIcon(
                        self.canvas,
                        x,
                        y,
                        device_config
                    )
                    
                    # Store the device
                    self.devices[device_config.name] = device
                
                # Update boundary containment after adding devices
                self.update_boundary_devices()
                messagebox.showinfo("Success", f"Added {len(devices)} devices successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add devices: {str(e)}")
        
        dialog = BulkDeviceDialog(self.root, add_devices)
        self.root.wait_window(dialog)
    def zoom_in(self):
        """Increase the zoom level of the canvas."""
        # Implement basic zoom by scaling canvas items
        for item in self.canvas.find_all():
            # Get current coordinates
            coords = self.canvas.coords(item)
            if coords:
                # Scale coordinates by 1.2 (20% larger)
                new_coords = [coord * 1.2 for coord in coords]
                self.canvas.coords(item, *new_coords)
                
                # Scale font size for text items
                if 'text' in self.canvas.type(item):
                    current_font = self.canvas.itemcget(item, 'font')
                    if isinstance(current_font, str):
                        font_size = int(current_font.split()[-1])
                        new_font = current_font.rsplit(' ', 1)[0] + f' {int(font_size * 1.2)}'
                        self.canvas.itemconfig(item, font=new_font)
        
        # Update zoom label
        current_zoom = int(self.zoom_label['text'].rstrip('%'))
        self.zoom_label['text'] = f"{int(current_zoom * 1.2)}%"
    def add_boundary_dialog(self):
        def add_boundary(config):
            # Create boundary with default size
            boundary = NetworkBoundary(
                self.canvas,
                x=100,
                y=100,
                width=300,
                height=200,
                config=config
            )
            self.boundaries[config.name] = boundary
            # Update contained devices
            self.update_boundary_devices()
        
        BoundaryDialog(self.root, add_boundary)
    def select_all(self, event=None):
        """Select all devices and boundaries in the topology."""
        # Select all devices
        for device in self.devices.values():
            device.highlight(True)
        
        # Select all boundaries
        for boundary in self.boundaries.values():
            boundary.highlight(True)
    def resize_start(self, event):
        handle_id = self.canvas.find_closest(event.x, event.y)[0]
        for boundary in self.boundaries.values():
            if boundary.resize_handle == handle_id:
                self.resizing_boundary = boundary
                self.resize_start = (event.x, event.y)
                break
    def export_topology(self, event=None):
            """Export the current topology as a PNG image."""
            try:
                # Get file path from user
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
                )
                if not file_path:
                    return

                # Get canvas bounds
                bbox = self.canvas.bbox("all")
                if not bbox:
                    messagebox.showwarning("Warning", "Nothing to export - canvas is empty!")
                    return

                # Adjust bbox to include some padding
                padding = 20
                x1, y1, x2, y2 = bbox
                bbox = (x1 - padding, y1 - padding, x2 + padding, y2 + padding)

                # Generate PostScript file
                ps_path = file_path + ".ps"
                self.canvas.postscript(file=ps_path, colormode='color', 
                                    pagewidth=x2-x1+2*padding,
                                    pageheight=y2-y1+2*padding,
                                    bbox=bbox)

                # Convert PostScript to PNG using PIL
                try:
                    from PIL import Image, ImageOps
                    import subprocess

                    # Try using Pillow's built-in PostScript support
                    with Image.open(ps_path) as img:
                        # Convert to RGB mode to ensure proper color handling
                        img = img.convert('RGB')
                        # Save as PNG
                        img.save(file_path, 'PNG')

                except Exception as e:
                    # If Pillow fails, try using system's convert command (ImageMagick)
                    try:
                        subprocess.run(['convert', ps_path, file_path], check=True)
                    except subprocess.CalledProcessError:
                        raise Exception("Failed to convert PostScript to PNG. Please install ImageMagick.")

                # Clean up temporary PostScript file
                import os
                try:
                    os.remove(ps_path)
                except:
                    pass  # Ignore cleanup errors

                messagebox.showinfo("Success", "Topology exported successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export topology: {str(e)}\n\n"
                                            "Make sure you have either PIL or ImageMagick installed.")

                # Cleanup any partial files
                import os
                try:
                    if 'ps_path' in locals() and os.path.exists(ps_path):
                        os.remove(ps_path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except:
                    pass  # Ignore cleanup errors
    def resize_boundary(self, event):
        if not self.resizing_boundary or not self.resize_start:
            return
        
        dx = event.x - self.resize_start[0]
        dy = event.y - self.resize_start[1]
        
        new_width = self.resizing_boundary.width + dx
        new_height = self.resizing_boundary.height + dy
        
        self.resizing_boundary.resize(new_width, new_height)
        self.resize_start = (event.x, event.y)
        # Update contained devices after resize
        self.update_boundary_devices()
    def save_topology(self, event=None):
            """Save the current topology to a JSON file."""
            topology = {
                'devices': [],
                'connections': [],
                'boundaries': []
            }
            
            # Save devices
            for device in self.devices.values():
                topology['devices'].append({
                    'name': device.config.name,
                    'type': device.config.device_type,
                    'ip': device.config.ip_address,
                    'x': device.x,
                    'y': device.y
                })
            
            # Save connections (avoid duplicates)
            seen_connections = set()
            for device in self.devices.values():
                for conn in device.connections:
                    # Create a unique identifier for the connection
                    conn_pair = tuple(sorted([conn.device1.config.name, conn.device2.config.name]))
                    if conn_pair not in seen_connections:
                        topology['connections'].append({
                            'device1': conn.device1.config.name,
                            'device2': conn.device2.config.name,
                            'type': conn.connection_type.value
                        })
                        seen_connections.add(conn_pair)
            
            # Save boundaries
            for boundary in self.boundaries.values():
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
            
            # Save to file
            try:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
                if file_path:
                    with open(file_path, 'w') as f:
                        json.dump(topology, f, indent=2)
                    messagebox.showinfo("Success", "Topology saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save topology: {str(e)}")
    def resize_stop(self, event):
        self.resizing_boundary = None
        self.resize_start = None
    def load_topology(self, event=None):
        """Load a topology from a JSON file."""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not file_path:
                return
                
            with open(file_path, 'r') as f:
                topology = json.load(f)
            
            # Clear current topology first
            self.new_topology()
            
            # Load boundaries first (bottom layer)
            for boundary_data in topology.get('boundaries', []):
                config = BoundaryConfig(
                    name=boundary_data['name'],
                    subnet=boundary_data['subnet'], 
                    description=boundary_data.get('description', ''),
                    color=boundary_data.get('color', '#E0E0E0')
                )
                boundary = NetworkBoundary(
                    self.canvas,
                    boundary_data['x'],
                    boundary_data['y'],
                    boundary_data['width'],
                    boundary_data['height'],
                    config
                )
                self.boundaries[config.name] = boundary
            
            # Load devices
            for device_data in topology.get('devices', []):
                config = DeviceConfig(
                    name=device_data['name'],
                    device_type=device_data['type'],
                    ip_address=device_data.get('ip', '')
                )
                device = DeviceIcon(
                    self.canvas,
                    device_data['x'],
                    device_data['y'],
                    config
                )
                self.devices[config.name] = device
            
            # Load connections last (top layer)
            for conn_data in topology.get('connections', []):
                if conn_data['device1'] in self.devices and conn_data['device2'] in self.devices:
                    device1 = self.devices[conn_data['device1']]
                    device2 = self.devices[conn_data['device2']]
                    conn_type = ConnectionType(conn_data.get('type', 'ethernet'))
                    Connection(self.canvas, device1, device2, conn_type)
            
            # Update boundary containment
            self.update_boundary_devices()
            
            messagebox.showinfo("Success", "Topology loaded successfully!")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file format!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load topology: {str(e)}")
    def canvas_click(self, event):
        if self.connecting:
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
                        self.create_connection(self.connection_start, clicked_device)
                    
                    self.connection_start.highlight(False)
                    self.connection_start = None
                    self.connecting = False
                    self.canvas.config(cursor="")
            return

        # First deselect all
        for device in self.devices.values():
            device.highlight(False)
        for boundary in self.boundaries.values():
            boundary.highlight(False)

        # Then check for clicks on devices or boundaries
        clicked_item = False

        # Check devices first (top layer)
        for device in self.devices.values():
            if device.contains(event.x, event.y):
                device.highlight(True)
                clicked_item = True
                print(f"Selected device: {device.config.name}")  # Debug print
                break

        # If no device was clicked, check boundaries
        if not clicked_item:
            for boundary in self.boundaries.values():
                if boundary.contains_point(event.x, event.y):
                    boundary.highlight(True)
                    clicked_item = True
                    print(f"Selected boundary: {boundary.config.name}")  # Debug print
                    break
    def new_topology(self, event=None):
            """Create a new empty topology after confirming with the user."""
            if self.devices or self.boundaries:
                if not messagebox.askyesno("New Topology", 
                    "Are you sure you want to create a new topology? All unsaved changes will be lost."):
                    return
            
            # Clear the canvas
            self.canvas.delete('all')
            
            # Reset all data structures
            self.devices.clear()
            self.boundaries.clear()
            
            # Reset states
            self.connecting = False
            self.connection_start = None
            self.resizing_boundary = None
            self.resize_start = None
            
            # Reset canvas view
            self.canvas.configure(scrollregion=(0, 0, 2000, 2000))
            
            # Reset cursor
            self.canvas.config(cursor="")
    def delete_selected(self):
        """Delete the currently selected device or boundary"""
        # Try to find selected device
        for name, device in list(self.devices.items()):  # Use list to avoid modification during iteration
            if device.selected:
                print(f"Deleting device: {name}")  # Debug print
                # Delete all connections first
                for conn in device.connections[:]:  # Use slice copy to avoid modification during iteration
                    conn.delete()
                # Delete the device
                self.canvas.delete(device.icon)
                self.canvas.delete(device.name_text)
                if hasattr(device, 'highlight_circle'):
                    self.canvas.delete(device.highlight_circle)
                del self.devices[name]
                return  # Exit after deleting one device

        # If no device was selected, try to find selected boundary
        for name, boundary in list(self.boundaries.items()):  # Use list to avoid modification during iteration
            if boundary.selected:
                print(f"Deleting boundary: {name}")  # Debug print
                self.canvas.delete(boundary.boundary)
                self.canvas.delete(boundary.name_text)
                self.canvas.delete(boundary.resize_handle)
                del self.boundaries[name]
                return  # Exit after deleting one boundary

        print("No item selected for deletion")  # Debug print

        def create_connection(self, device1, device2):
            connection_dialog = tk.Toplevel(self.root)
            connection_dialog.title("Select Connection Type")
            connection_dialog.transient(self.root)
            connection_dialog.grab_set()
            
            conn_type = tk.StringVar(value=ConnectionType.ETHERNET.value)
            
            for ctype in ConnectionType:
                ttk.Radiobutton(
                    connection_dialog,
                    text=ctype.value.title(),
                    variable=conn_type,
                    value=ctype.value
                ).pack(anchor='w', padx=5, pady=2)
                
            def apply():
                Connection(
                    self.canvas,
                    device1,
                    device2,
                    ConnectionType(conn_type.get())
                )
                connection_dialog.destroy()
            
            ttk.Button(
                connection_dialog,
                text="Connect",
                command=apply
            ).pack(pady=10)