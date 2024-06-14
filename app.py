import tkinter as tk
from tkinter import filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter import plot_data_across_dates
import matplotlib.pyplot as plt
from tkinter import messagebox


# Function to load the Excel file
def load_file():
    global df, location_options, room_options, panel_options, parameter_options
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            show_info("File loaded successfully")

            # Populate dropdown options with distinct values from respective columns
            location_options = df["Location"].dropna().unique().tolist()
            room_options = df["Room"].dropna().unique().tolist()
            panel_options = df["Panel"].dropna().unique().tolist()
            parameter_options = df["Parameter Line"].dropna().unique().tolist()
            # Update the OptionMenus
            update_option_menus()
        except Exception as e:
            show_error(f"Failed to load file: {e}")


def update_option_menus():
    location_var.set(location_options[0] if location_options else "")
    room_var.set(room_options[0] if room_options else "")
    panel_var.set(panel_options[0] if panel_options else "")
    parameter_var.set(parameter_options[0] if parameter_options else "")

    location_menu['menu'].delete(0, 'end')
    room_menu['menu'].delete(0, 'end')
    panel_menu['menu'].delete(0, 'end')
    parameter_menu['menu'].delete(0, 'end')

    for option in location_options:
        location_menu['menu'].add_command(label=option, command=tk._setit(location_var, option))
    for option in room_options:
        room_menu['menu'].add_command(label=option, command=tk._setit(room_var, option))
    for option in panel_options:
        panel_menu['menu'].add_command(label=option, command=tk._setit(panel_var, option))
    for option in parameter_options:
        parameter_menu['menu'].add_command(label=option, command=tk._setit(parameter_var, option))


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
    # Call data with the loaded df and canvas
    try:
        plot_data_across_dates(df, canvas, location, room, panel, parameter)
    except Exception as e:
        show_error(f"Graph plotting failed: {e}")


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
window.title("LitUp Excel Plotter")

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

# Initialize empty options
location_options = [""]
room_options = [""]
panel_options = [""]
parameter_options = [""]
location_var.set(location_options[0])
room_var.set(room_options[0])
panel_var.set(panel_options[0])
parameter_var.set(parameter_options[0])

# Create dropdowns with initial empty values
tk.Label(control_frame, text="Location:").pack(side=tk.LEFT, padx=5)
location_menu = tk.OptionMenu(control_frame, location_var, *location_options)
location_menu.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame, text="Room:").pack(side=tk.LEFT, padx=5)
room_menu = tk.OptionMenu(control_frame, room_var, *room_options)
room_menu.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame, text="Panel:").pack(side=tk.LEFT, padx=5)
panel_menu = tk.OptionMenu(control_frame, panel_var, *panel_options)
panel_menu.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame, text="Parameter:").pack(side=tk.LEFT, padx=5)
parameter_menu = tk.OptionMenu(control_frame, parameter_var, *parameter_options)
parameter_menu.pack(side=tk.LEFT, padx=5)

# Run the main application loop
window.mainloop()
