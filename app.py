import tkinter as tk
from tkinter import filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter import plot_voltage_data
import matplotlib.pyplot as plt
from tkinter import messagebox
# Function to load the Excel file
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            show_info("File loaded successfully")
        except:
            show_error("Failed to load file")
# Function to plot the data using plotter.plot_voltage_data
def plot_data():
    global df, canvas
    if 'df' not in globals():
        show_warning("Please load the file first")
        return
    location = location_var.get()
    room = room_var.get()
    panel = panel_var.get()
    parameter = parameter_var.get()
    # Call plot_voltage_data with the loaded df and canvas
    try:
        plot_voltage_data(df, canvas, location, room, panel, parameter)
    except:
        show_error("Graph plotting failed")
# Display error messages

def show_info(message, timeout=1000):
    popup = tk.Toplevel()
    popup.title("Information")
    tk.Label(popup, text=message).pack(pady=10, padx=10)
    popup.after(timeout, popup.destroy)
def show_warning(message, timeout=2000):
    popup = tk.Toplevel()
    popup.title("Warning")
    tk.Label(popup, text=message).pack(pady=10, padx=10)
    popup.after(timeout, popup.destroy)
def show_error(message):
    messagebox.showerror("Error", message)

# Create the main application window
window = tk.Tk()
window.title("Voltage Plotter")

# Create a frame for buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

# Load File button
load_button = tk.Button(button_frame, text="Load File", command=load_file)
load_button.pack(side=tk.LEFT, padx=10)

# Plot Data button
plot_button = tk.Button(button_frame, text="Plot Data", command=plot_data)
plot_button.pack(side=tk.LEFT, padx=10)

# Create a canvas for the plot
canvas_frame = tk.Frame(window)
canvas_frame.pack(fill=tk.BOTH, expand=True)

canvas = FigureCanvasTkAgg(plt.figure(), master=canvas_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Dropdown Frame
control_frame = tk.Frame(window)
control_frame.pack(pady=10)

# Dropdown menus
location_var = tk.StringVar(window)
room_var = tk.StringVar(window)
panel_var = tk.StringVar(window)
parameter_var = tk.StringVar(window)


# Example options
location_options = ["CLS", "Location 2", "Location 3"]
room_options = ["Switch Room", "Room 2", "Room 3"]
panel_options = ["MSB R", "Panel 2", "Panel 3"]
parameter_options = ["L-L (Volt)", "Parameter 2", "Parameter 3"]

# Set default values
location_var.set(location_options[0])
room_var.set(room_options[0])
panel_var.set(panel_options[0])
parameter_var.set(parameter_options[0])

# Create dropdowns
tk.Label(control_frame, text="Location:").pack(side=tk.LEFT, padx=5)
tk.OptionMenu(control_frame, location_var, *location_options).pack(side=tk.LEFT, padx=5)
tk.Label(control_frame, text="Room:").pack(side=tk.LEFT, padx=5)
tk.OptionMenu(control_frame, room_var, *room_options).pack(side=tk.LEFT, padx=5)
tk.Label(control_frame, text="Panel:").pack(side=tk.LEFT, padx=5)
tk.OptionMenu(control_frame, panel_var, *panel_options).pack(side=tk.LEFT, padx=5)
tk.Label(control_frame, text="Parameter:").pack(side=tk.LEFT, padx=5)
tk.OptionMenu(control_frame, parameter_var, *parameter_options).pack(side=tk.LEFT, padx=5)

# Run the main application loop
window.mainloop()
