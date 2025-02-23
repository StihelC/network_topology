# Network Topology Designer

A Python-based network topology design tool that allows users to create, edit, and visualize network diagrams with drag-and-drop functionality.

## Features

- **Interactive Canvas**
  - Drag and drop devices
  - Create connections between devices
  - Draw boundary regions
  - Zoom in/out functionality
  - Pan navigation

- **Device Management**
  - Multiple device types
  - Custom device properties
  - Device grouping
  - Visual device states

- **Connection Types**
  - Ethernet
  - Fiber
  - Wireless
  - VPN
  - Serial
  - USB

## Project Structure

```bash
network_topology/
├── gui/
│   ├── __init__.py
│   ├── canvas_panel.py     # Main drawing area
│   ├── main_window.py      # Application window
│   ├── menu_bar.py         # Menu system
│   ├── properties_panel.py # Device/boundary properties
│   └── toolbar.py         # Tool shortcuts
├── models/
│   ├── __init__.py
│   ├── boundary.py        # Boundary region logic
│   ├── connection.py      # Connection management
│   ├── device.py         # Device representation
│   └── enums.py          # Enumerations
├── icons/                 # Device and UI icons
├── tests/                 # Unit tests
├── main.py               # Application entry point
└── requirements.txt      # Dependencies
```

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/network_topology.git
cd network_topology
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

## Usage Guide

### Basic Operations

#### Adding Devices
1. Click the device button in toolbar
2. Click on canvas to place device
3. Configure device properties in the properties panel

#### Creating Connections
1. Select connection type from the toolbar
2. Click source device
3. Click target device to complete connection

#### Drawing Boundaries
1. Click boundary button in toolbar
2. Click and drag to define area
3. Adjust size using corner handles

#### Navigation
- **Zoom**: `Ctrl + Mouse Wheel`
- **Pan**: `Middle Mouse Button`
- **Select**: `Left Click`
- **Delete**: `Delete Key`

## Development

### Dependencies

```python
# filepath: /home/cam/Desktop/network_topology/requirements.txt
pillow>=10.0.0
tkinter
pytest>=7.0.0
```

### Code Organization

#### GUI Components
- `NetworkTopologyGUI`: Main application window
- `CanvasPanel`: Interactive drawing surface
- `MenuBar`: Application menus
- `Toolbar`: Quick access tools
- `PropertiesPanel`: Element properties

#### Models
- `Device`: Network device representation
- `Connection`: Connection management
- `Boundary`: Grouping boundaries
- `Enums`: Type definitions

### Development Guidelines

1. **Code Style**
   - Follow PEP 8
   - Use type hints
   - Document classes and methods
   - Use meaningful variable names

2. **Testing**
   ```bash
   # Run tests
   pytest tests/
   ```

3. **Adding Features**
   - Create feature branch
   - Implement changes
   - Add tests
   - Update documentation
   - Submit pull request

## Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Icons from [Material Design Icons](https://materialdesignicons.com/)
- Network topology concepts from [Cisco Network Design](https://www.cisco.com/c/en/us/solutions/design-zone.html)

---

## Development Status

This project is under active development. Features and documentation may change.

### Upcoming Features
- [ ] Network simulation
- [ ] Export to various formats
- [ ] Device templates
- [ ] Network validation
- [ ] Custom icon support

### Known Issues
- Device dragging needs optimization
- Connection line rendering improvements needed
- Boundary resize handles need refinement

For more detailed information, please refer to the [documentation](docs/index.md).