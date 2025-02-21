import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import ipaddress
from models import DeviceConfig

class BulkDeviceDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Bulk Add Devices")
        self.callback = callback
        
        # Set window size and make it resizable
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Create main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create table
        self.create_table()
        
        # Create buttons
        self.create_buttons()
        
        # Add initial empty row
        self.add_empty_row()

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

    def create_table(self):
        # Create table frame with scrollbar
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(self.table_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        self.scrollbar.config(command=self.canvas.yview)
        
        # Frame for rows
        self.rows_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor=tk.NW)
        
        # Headers
        self.create_headers()
        
        # Configure scroll region
        self.rows_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Store rows
        self.rows = []

    def on_canvas_configure(self, event):
        # Update the scroll region to encompass the inner frame
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def create_headers(self):
        headers = ["Device Name", "Device Type", "IP Address", ""]
        header_frame = ttk.Frame(self.rows_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for i, header in enumerate(headers):
            label = ttk.Label(header_frame, text=header, font=('Arial', 10, 'bold'))
            label.grid(row=0, column=i, padx=5, sticky=tk.W)
            
        header_frame.grid_columnconfigure(3, weight=1)

    def create_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Add Row", command=self.add_empty_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Import CSV", command=self.import_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Devices", command=self.submit).pack(side=tk.RIGHT, padx=5)

    def add_empty_row(self):
        row_frame = ttk.Frame(self.rows_frame)
        row_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Device name entry
        name_entry = ttk.Entry(row_frame)
        name_entry.grid(row=0, column=0, padx=5, sticky='ew')
        
        # Device type combobox
        device_types = ['router', 'switch', 'firewall', 'server', 'client', 'access_point']
        type_var = tk.StringVar(value=device_types[0])
        type_combo = ttk.Combobox(row_frame, textvariable=type_var, values=device_types, state='readonly')
        type_combo.grid(row=0, column=1, padx=5, sticky='ew')
        
        # IP address entry
        ip_entry = ttk.Entry(row_frame)
        ip_entry.grid(row=0, column=2, padx=5, sticky='ew')
        
        # Delete button
        delete_btn = ttk.Button(row_frame, text="X", width=3,
                              command=lambda: self.delete_row(row_frame))
        delete_btn.grid(row=0, column=3, padx=5)
        
        # Configure grid weights
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=1)
        row_frame.grid_columnconfigure(2, weight=1)
        
        # Store row info
        self.rows.append({
            'frame': row_frame,
            'name': name_entry,
            'type': type_combo,
            'ip': ip_entry
        })
        
        # Update scroll region
        self.on_frame_configure()

    def delete_row(self, row_frame):
        if len(self.rows) > 1:  # Keep at least one row
            row_frame.destroy()
            self.rows = [row for row in self.rows if row['frame'] != row_frame]
            self.on_frame_configure()

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def validate_ip(self, ip):
        if not ip:  # Allow empty IP
            return True
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def import_csv(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not file_path:
                return
                
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames
                
                # Clear existing rows
                for row_data in self.rows:
                    row_data['frame'].destroy()
                self.rows = []
                
                for row in reader:
                    self.add_empty_row()
                    current_row = self.rows[-1]
                    
                    # Fill in the data
                    current_row['name'].insert(0, row.get('name', ''))
                    current_row['type'].set(row.get('type', 'router'))
                    current_row['ip'].insert(0, row.get('ip', ''))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import CSV: {str(e)}")

    def submit(self):
        devices = []
        errors = []
        
        print("Submit clicked - Processing rows")  # Debug print
        for idx, row in enumerate(self.rows, 1):
            name = row['name'].get().strip()
            device_type = row['type'].get()
            ip = row['ip'].get().strip()
            
            print(f"Processing row {idx}: name={name}, type={device_type}, ip={ip}")  # Debug print
            
            # Validate entries
            if not name:
                errors.append(f"Row {idx}: Device name is required")
                continue
                
            if ip and not self.validate_ip(ip):
                errors.append(f"Row {idx}: Invalid IP address")
                continue
            
            # Create device config
            device = DeviceConfig(
                name=name,
                device_type=device_type,
                ip_address=ip
            )
            devices.append(device)
            print(f"Added device {name} to list")  # Debug print
        
        if errors:
            print(f"Validation errors: {errors}")  # Debug print
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        # Call callback with valid devices
        if devices:
            print(f"Calling callback with {len(devices)} devices")  # Debug print
            self.callback(devices)
            self.destroy()
        else:
            print("No valid devices to add")  # Debug print
            messagebox.showerror("Error", "No valid devices to add")