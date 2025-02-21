#!/usr/bin/env python3
import tkinter as tk
from gui.main_window import NetworkTopologyGUI

def main():
    root = tk.Tk()
    root.title("Network Topology Designer")
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Center window on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1024
    window_height = 768
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = NetworkTopologyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()