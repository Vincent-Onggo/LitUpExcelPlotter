import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter import plot_data_across_dates
import matplotlib.pyplot as plt
from matplotlib import figure

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

            # Add a null option to the dropdown options
            location_options.insert(len(location_options), "")
            room_options.insert(len(room_options), "")
            panel_options.insert(len(panel_options), "")
            parameter_options.insert(len(parameter_options), "")

            # Update the OptionMenus
            update_option_menus()
        except Exception as e:
            show_error(f"Failed to load file: {e}")


def update_option_menus():
    location_var1.set(location_options[0] if location_options else "")
    room_var1.set(room_options[0] if room_options else "")
    panel_var1.set(panel_options[0] if panel_options else "")
    parameter_var1.set(parameter_options[0] if parameter_options else "")

    location_var2.set("")
    room_var2.set("")
    panel_var2.set("")
    parameter_var2.set("")

    location_menu1['menu'].delete(0, 'end')
    room_menu1['menu'].delete(0, 'end')
    panel_menu1['menu'].delete(0, 'end')
    parameter_menu1['menu'].delete(0, 'end')

    location_menu2['menu'].delete(0, 'end')
    room_menu2['menu'].delete(0, 'end')
    panel_menu2['menu'].delete(0, 'end')
    parameter_menu2['menu'].delete(0, 'end')

    for option in location_options:
        location_menu1['menu'].add_command(label=option, command=tk._setit(location_var1, option))
        location_menu2['menu'].add_command(label=option, command=tk._setit(location_var2, option))
    for option in room_options:
        room_menu1['menu'].add_command(label=option, command=tk._setit(room_var1, option))
        room_menu2['menu'].add_command(label=option, command=tk._setit(room_var2, option))
    for option in panel_options:
        panel_menu1['menu'].add_command(label=option, command=tk._setit(panel_var1, option))
        panel_menu2['menu'].add_command(label=option, command=tk._setit(panel_var2, option))
    for option in parameter_options:
        parameter_menu1['menu'].add_command(label=option, command=tk._setit(parameter_var1, option))
        parameter_menu2['menu'].add_command(label=option, command=tk._setit(parameter_var2, option))


# Function to plot the data using plotter.plot_data_across_dates
def plot_data():
    global df, canvas
    if 'df' not in globals():
        show_warning("Please load the file first")
        return
    location1 = location_var1.get()
    room1 = room_var1.get()
    panel1 = panel_var1.get()
    parameter1 = parameter_var1.get()

    location2 = location_var2.get()
    room2 = room_var2.get()
    panel2 = panel_var2.get()
    parameter2 = parameter_var2.get()

    try:
        plot_data_across_dates(df, canvas,
                               [(location1, room1, panel1, parameter1), (location2, room2, panel2, parameter2)],
                               label_frame)
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

# Dropdown Frame for first set of parameters
control_frame1 = tk.Frame(window)
control_frame1.pack(pady=10)

# Dropdown menus for first set of parameters
location_var1 = tk.StringVar(window)
room_var1 = tk.StringVar(window)
panel_var1 = tk.StringVar(window)
parameter_var1 = tk.StringVar(window)

location_options = [""]
room_options = [""]
panel_options = [""]
parameter_options = [""]
location_var1.set(location_options[0])
room_var1.set(room_options[0])
panel_var1.set(panel_options[0])
parameter_var1.set(parameter_options[0])

tk.Label(control_frame1, text="Location:").pack(side=tk.LEFT, padx=5)
location_menu1 = tk.OptionMenu(control_frame1, location_var1, *location_options)
location_menu1.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame1, text="Room:").pack(side=tk.LEFT, padx=5)
room_menu1 = tk.OptionMenu(control_frame1, room_var1, *room_options)
room_menu1.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame1, text="Panel:").pack(side=tk.LEFT, padx=5)
panel_menu1 = tk.OptionMenu(control_frame1, panel_var1, *panel_options)
panel_menu1.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame1, text="Parameter:").pack(side=tk.LEFT, padx=5)
parameter_menu1 = tk.OptionMenu(control_frame1, parameter_var1, *parameter_options)
parameter_menu1.pack(side=tk.LEFT, padx=5)

# Dropdown Frame for second set of parameters
control_frame2 = tk.Frame(window)
control_frame2.pack(pady=10)

# Dropdown menus for second set of parameters
location_var2 = tk.StringVar(window)
room_var2 = tk.StringVar(window)
panel_var2 = tk.StringVar(window)
parameter_var2 = tk.StringVar(window)

location_var2.set(location_options[0])
room_var2.set(room_options[0])
panel_var2.set(panel_options[0])
parameter_var2.set(parameter_options[0])

tk.Label(control_frame2, text="Location:").pack(side=tk.LEFT, padx=5)
location_menu2 = tk.OptionMenu(control_frame2, location_var2, *location_options)
location_menu2.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame2, text="Room:").pack(side=tk.LEFT, padx=5)
room_menu2 = tk.OptionMenu(control_frame2, room_var2, *room_options)
room_menu2.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame2, text="Panel:").pack(side=tk.LEFT, padx=5)
panel_menu2 = tk.OptionMenu(control_frame2, panel_var2, *panel_options)
panel_menu2.pack(side=tk.LEFT, padx=5)
tk.Label(control_frame2, text="Parameter:").pack(side=tk.LEFT, padx=5)
parameter_menu2 = tk.OptionMenu(control_frame2, parameter_var2, *parameter_options)
parameter_menu2.pack(side=tk.LEFT, padx=5)

# Create a frame for labels
label_frame = tk.Frame(window)
label_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10, anchor='se')

# Run the main application loop
window.mainloop()
