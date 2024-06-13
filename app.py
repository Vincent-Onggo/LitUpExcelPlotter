import tkinter as tk
from tkinter import filedialog
import pandas as pd
from plotter import plot_voltage_data

# Function to load the Excel file
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        df = pd.read_excel(file_path)
        print("File loaded successfully.")

# Function to plot the data using plotter.plot_voltage_data
def plot_data():
    global df
    if 'df' not in globals():
        print("Please load the file first.")
        return

    plot_voltage_data("data.xlsx", "Daily Log Site", "CLS", "Switch Room", "MSB R", "L-L (Volt)")  # Call plot_voltage_data from plotter module

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

# Run the main application loop
window.mainloop()
