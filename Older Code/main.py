import tkinter as tk
from tkinter import Menu
from network_topology_gui import NetworkTopologyGUI

def main():
    root = tk.Tk()
    app = NetworkTopologyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

class NetworkTopologyGUI:
    def __init__(self, root):
        self.root = root
        self.create_menu()

    def create_menu(self):
        file_menu = Menu(self.root)
        file_menu.add_command(label="New", command=self.new_topology)
        # Add other menu items here

    def new_topology(self):
        # Define what happens when "New" is clicked
        print("New topology created")