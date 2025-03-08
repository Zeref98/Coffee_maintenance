# main.py
import tkinter as tk
from maintenance_app import MaintenanceApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()
