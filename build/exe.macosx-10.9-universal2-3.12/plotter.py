import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import tkinter as tk


def plot_data_across_dates(df, canvas, filter_sets, label_frame):
    # Clear the current plot
    canvas.figure.clf()

    fig = canvas.figure
    ax = fig.add_subplot(111)

    for filters in filter_sets:
        if all(filters):  # Only proceed if none of the filters are null
            location_, room_, panel_, parameter_line_ = filters

            # Filter the data
            filtered_df = df[(df['Location'] == location_) &
                             (df['Room'] == room_) &
                             (df['Panel'] == panel_) &
                             (df['Parameter Line'] == parameter_line_)]

            if filtered_df.empty:
                continue

            # Assuming the dates are in columns and the structure is similar to the screenshot
            dates = filtered_df.columns[5:]  # Adjust index based on the structure of your Excel file
            values = filtered_df.iloc[0, 5:].values  # Adjust index based on the structure of your Excel file

            # Create a DataFrame for plotting
            plot_df = pd.DataFrame({"Date": dates, parameter_line_: values})

            # Clean the data
            plot_df = clean_data(plot_df, parameter_line_)

            # Plotting the data
            ax.plot(plot_df["Date"], plot_df[parameter_line_], marker='o', linestyle='-',
                    label=f"{parameter_line_} ({location_}, {room_}, {panel_})")

            # Highlight min and max data points with different colors
            min_value = plot_df[parameter_line_].min()
            max_value = plot_df[parameter_line_].max()

            ax.scatter(plot_df["Date"].loc[plot_df[parameter_line_] == min_value].iloc[:1], min_value, color='red',
                       s=300,
                       label=f"Min {parameter_line_} ({location_}, {room_}, {panel_})")
            ax.scatter(plot_df["Date"].loc[plot_df[parameter_line_] == max_value].iloc[:1], max_value, color='green',
                       s=300,
                       label=f"Max {parameter_line_} ({location_}, {room_}, {panel_})")

    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.set_title("Data across different dates")
    ax.grid(True)

    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to be every month
    fig.autofmt_xdate()

    # Add a legend for the main plot
    ax.legend()

    # Update canvas and label frame
    canvas.draw()
    label_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10, anchor='se')


def clean_data(df, parameter_type):
    # Make a copy of the DataFrame to avoid SettingWithCopyWarning
    df = df.copy()

    # Remove any rows where the date is not in the expected format
    df = df[df['Date'].str.contains('-')]

    # Replace ,, with . and then replace , with .
    df.loc[:, parameter_type] = df[parameter_type].str.replace(',,', '.', regex=False).str.replace(',', '.',
                                                                                                   regex=False)

    # Convert values to numeric, handling errors
    df.loc[:, parameter_type] = pd.to_numeric(df[parameter_type], errors='coerce')

    # Drop rows with NaN values in the parameter column
    df.dropna(subset=[parameter_type], inplace=True)
    return df
