from models import ConnectionType

class Connection:
    LINE_STYLES = {
        ConnectionType.ETHERNET: {'dash': None, 'width': 2, 'color': '#2196F3'},
        ConnectionType.FIBER: {'dash': (5,), 'width': 2, 'color': '#FF9800'},
        ConnectionType.WIRELESS: {'dash': (2, 4), 'width': 1, 'color': '#4CAF50'},
        ConnectionType.VPN: {'dash': (8, 4), 'width': 2, 'color': '#9C27B0'},
        ConnectionType.SERIAL: {'dash': (2, 2), 'width': 1, 'color': '#607D8B'},
        ConnectionType.USB: {'dash': (4, 2), 'width': 1, 'color': '#795548'}
    }

    def __init__(self, canvas, device1, device2, connection_type=ConnectionType.ETHERNET):
        """
        Initialize a new connection.

        :param canvas: The canvas on which to draw the connection.
        :param device1: The first device in the connection.
        :param device2: The second device in the connection.
        :param connection_type: The type of the connection (default is ConnectionType.ETHERNET).
        """
        self.canvas = canvas
    def __init__(self, canvas, device1, device2, connection_type=ConnectionType.ETHERNET):
        """
        Initialize a new connection.

        :param canvas: The canvas on which to draw the connection.
        :param device1: The first device in the connection.
        :param device2: The second device in the connection.
        :param connection_type: The type of the connection (default is ConnectionType.ETHERNET).
        """
        self.canvas = canvas
        self.device1 = device1
        self.device2 = device2
        self.connection_type = connection_type
        self.line = None
        self.create_line()
        device1.connections.append(self)
        device2.connections.append(self)

    def update_position(self):
        """
        Update the position of the connection line on the canvas.
        
        This method retrieves the current positions of the connected devices
        and updates the coordinates of the line representing the connection.
        """
        x1, y1 = self.device1.get_position()
        x2, y2 = self.device2.get_position()
        style = self.LINE_STYLES[self.connection_type]
        self.line = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=style['color'],
            width=style['width'],
            dash=style['dash']
        )
        self.canvas.tag_lower(self.line)
    def delete(self):
        """
        Deletes the connection from the canvas and removes it from the devices' connection lists.
        """
    def update_position(self):
        x1, y1 = self.device1.get_position()
        x2, y2 = self.device2.get_position()
        self.canvas.coords(self.line, x1, y1, x2, y2)

    def delete(self):
        self.canvas.delete(self.line)
        self.device1.connections.remove(self)
        self.device2.connections.remove(self)