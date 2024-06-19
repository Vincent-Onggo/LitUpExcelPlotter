import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import tkinter as tk


def plot_data_across_dates(df, canvas, filter_sets, label_frame):
    """
    Filters the data based on the given parameters and plots the data across dates.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        canvas (FigureCanvasTkAgg): The Tkinter canvas to draw the plot.
        filter_sets (list of tuples): Each tuple contains (location, room, panel, parameter_line).
        label_frame (tk.Frame): The Tkinter frame to display mean, min, and max values.
    """
    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    for filters in filter_sets:
        location_, room_, panel_, parameter_line_ = filters

        # Filter the data
        filtered_df = df[(df['Location'] == location_) &
                         (df['Room'] == room_) &
                         (df['Panel'] == panel_) &
                         (df['Parameter Line'] == parameter_line_)]

        if filtered_df.empty:
            raise ValueError("No data found for the given filters")

        # Assuming the dates are in columns starting from the 6th column
        dates = filtered_df.columns[5:]  # Adjust index based on the structure of your Excel file
        values = filtered_df.iloc[0, 5:].values  # Adjust index based on the structure of your Excel file

        # Create a DataFrame for plotting
        plot_df = pd.DataFrame({"Date": dates, parameter_line_: values})

        # Clean the data
        plot_df = clean_data(plot_df, parameter_line_)

        # Plotting the data
        ax.plot(plot_df["Date"], plot_df[parameter_line_], marker='o', linestyle='-',
                label=f'{parameter_line_} ({location_}, {room_}, {panel_})')

        # Calculate mean, min, max values
        min_value = plot_df[parameter_line_].min()
        max_value = plot_df[parameter_line_].max()
        mean_value = plot_df[parameter_line_].mean()

        # Highlight min and max data points with different colors
        ax.scatter(plot_df["Date"].loc[plot_df[parameter_line_] == min_value].iloc[:1], min_value, s=100,
                   label=f"Min {parameter_line_} ({location_}, {room_}, {panel_})")
        ax.scatter(plot_df["Date"].loc[plot_df[parameter_line_] == max_value].iloc[:1], max_value, s=100,
                   label=f"Max {parameter_line_} ({location_}, {room_}, {panel_})")

        # Update labels for mean, min, and max values
        update_labels(label_frame, mean_value, min_value, max_value, parameter_line_, location_, room_, panel_)

    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.set_title(f"Data across different dates")
    ax.legend()
    ax.grid(True)

    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to be every month
    fig.autofmt_xdate()

    # Draw the plot on the Tkinter canvas
    canvas.figure = fig
    canvas.draw()


def clean_data(df, parameter_type):
    """
    Cleans the data by removing invalid dates, replacing value separators, and converting to numeric.

    Args:
        df (pd.DataFrame): The dataframe to be cleaned.
        parameter_type (str): The parameter type column to be cleaned.

    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    df = df.copy()

    # Remove any rows where the date is not in the expected format
    df = df[df['Date'].str.contains('-')]

    # Replace ,, with . and then replace , with .
    df[parameter_type] = df[parameter_type].str.replace(',,', '.', regex=False).str.replace(',', '.', regex=False)

    # Convert values to numeric, handling errors
    df[parameter_type] = pd.to_numeric(df[parameter_type], errors='coerce')

    # Drop rows with NaN values in the parameter column
    df.dropna(subset=[parameter_type], inplace=True)

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)

    return df


def update_labels(label_frame, mean_value, min_value, max_value, parameter_type, location, room, panel):
    """
    Updates the labels in the label frame with mean, min, and max values.

    Args:
        label_frame (tk.Frame): The Tkinter frame to display mean, min, and max values.
        mean_value (float): The mean value.
        min_value (float): The minimum value.
        max_value (float): The maximum value.
        parameter_type (str): The parameter type.
        location (str): The location.
        room (str): The room.
        panel (str): The panel.
    """
    # Clear existing labels
    for widget in label_frame.winfo_children():
        widget.destroy()

    # Create new labels with the updated values
    mean_label = tk.Label(label_frame, text=f"Mean {parameter_type} ({location}, {room}, {panel}): {mean_value:.2f}")
    min_label = tk.Label(label_frame, text=f"Min {parameter_type} ({location}, {room}, {panel}): {min_value:.2f}")
    max_label = tk.Label(label_frame, text=f"Max {parameter_type} ({location}, {room}, {panel}): {max_value:.2f}")

    # Pack the labels into the label frame
    mean_label.pack(side=tk.RIGHT, padx=5)
    min_label.pack(side=tk.RIGHT, padx=5)
    max_label.pack(side=tk.RIGHT, padx=5)
