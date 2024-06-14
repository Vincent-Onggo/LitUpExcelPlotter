import tkinter as tk
from tkinter import filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter import plot_voltage_data
import matplotlib.pyplot as plt

# Function to load the Excel file
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        df = pd.read_excel(file_path)
        print("File loaded successfully.")

# Function to plot the data using plotter.plot_voltage_data
def plot_data():
    global df, canvas
    if 'df' not in globals():
        print("Please load the file first.")
        return

    # Call plot_voltage_data with the loaded df and canvas
    plot_voltage_data(df, canvas, "CLS", "Switch Room", "MSB R", "L-L (Volt)")

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

# Run the main application loop
window.mainloop()
