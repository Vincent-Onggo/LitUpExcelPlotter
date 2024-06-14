import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.figure import Figure

def plot_data_across_dates(df, canvas, location_, room_, panel_, parameter_line_):
    # Filter the data
    filtered_df = df[(df['Location'] == location_) &
                     (df['Room'] == room_) &
                     (df['Panel'] == panel_) &
                     (df['Parameter Line'] == parameter_line_)]

    # Assuming the dates are in columns and the structure is similar to the screenshot
    dates = filtered_df.columns[5:]  # Adjust index based on the structure of your Excel file
    values = filtered_df.iloc[0, 5:].values  # Adjust index based on the structure of your Excel file

    # Create a DataFrame for plotting
    plot_df = pd.DataFrame({"Date": dates, parameter_line_: values})

    # Clean the data
    plot_df = clean_data(plot_df, parameter_line_)

    # Plotting the data
    plot_graph(plot_df, canvas, parameter_line_)


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
    print(df)
    return df


def plot_graph(df, canvas, parameter_type):
    # Create a new figure
    fig = Figure(figsize=(25, 10))
    ax = fig.add_subplot(111)

    # Plotting the data
    ax.plot(df["Date"], df[parameter_type], marker='o', linestyle='-', color='b')
    ax.set_xlabel("Date")
    ax.set_ylabel(parameter_type)
    ax.set_title(f"{parameter_type} across different dates")
    ax.grid(True)

    # Calculate mean, min, max values
    min_value = df[parameter_type].min()
    max_value = df[parameter_type].max()
    mean_value = df[parameter_type].mean()
    print("Date: ", len(df["Date"]))
    print("Values: ", len(df[parameter_type]))

    # Print out the actual values of Date and parameter_type columns
    print("Date values:", df["Date"].tolist())
    print("parameter_type values:", df[parameter_type].tolist())
    # Highlight min and max data points with different colors
    ax.scatter(df["Date"].loc[df[parameter_type] == min_value].iloc[:1], min_value, color='red', s=300, label=f"Min {parameter_type}")
    ax.scatter(df["Date"].loc[df[parameter_type] == max_value].iloc[:1], max_value, color='green', s=300,
               label=f"Max {parameter_type}")

    # Add a legend for the main plot
    ax.legend()
    # Add a separate legend for min, max, and mean values
    fig.text(0.15, 0.2, f"Min {parameter_type}: {min_value:.2f}", color='red')
    fig.text(0.15, 0.23, f"Max {parameter_type}: {max_value:.2f}", color='green')
    fig.text(0.15, 0.26, f"Mean {parameter_type}: {mean_value:.2f}", color='blue')

    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to be every month
    fig.autofmt_xdate()
    # Draw the plot on the Tkinter canvas
    canvas.figure = fig
    canvas.draw()
