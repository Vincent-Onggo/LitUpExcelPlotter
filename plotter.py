import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

def plot_voltage_data(file_path, sheet_name, location, room, panel, parameter_line):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Filter the data
    filtered_df = df[(df['Location'] == location) &
                     (df['Room'] == room) &
                     (df['Panel'] == panel) &
                     (df['Parameter Line'] == parameter_line)]

    # Assuming the dates are in columns and the structure is similar to the screenshot
    dates = filtered_df.columns[5:]  # Adjust index based on the structure of your Excel file
    voltages = filtered_df.iloc[0, 5:].values  # Adjust index based on the structure of your Excel file

    # Create a DataFrame for plotting
    plot_df = pd.DataFrame({"Date": dates, "Voltage (L-L)": voltages})

    # Clean the data
    plot_df = clean_data(plot_df)

    # Plotting the data
    plot_graph(plot_df)

def clean_data(df):
    # Make a copy of the DataFrame to avoid SettingWithCopyWarning
    df = df.copy()

    # Remove any rows where the date is not in the expected format
    df = df[df['Date'].str.contains('-')]

    # Replace ,, with . and then replace , with .
    df.loc[:, "Voltage (L-L)"] = df["Voltage (L-L)"].str.replace(',,', '.', regex=False).str.replace(',', '.', regex=False)

    # Convert voltage values to numeric, handling errors
    df.loc[:, "Voltage (L-L)"] = pd.to_numeric(df["Voltage (L-L)"], errors='coerce')

    # Drop rows with NaN values in 'Voltage (L-L)'
    df.dropna(subset=["Voltage (L-L)"], inplace=True)
    print(df)
    return df

def plot_graph(df):
    # Plotting the data
    plt.figure(figsize=(15, 10))
    plt.plot(df["Date"], df["Voltage (L-L)"], marker='o', linestyle='-', color='b')
    plt.xlabel("Date")
    plt.ylabel("Voltage (L-L)")
    plt.title("Voltage across different dates")
    plt.grid(True)

    # Calculate mean, min, max values
    min_voltage = df["Voltage (L-L)"].min()
    max_voltage = df["Voltage (L-L)"].max()
    mean_voltage = df["Voltage (L-L)"].mean()

    # Highlight min and max data points with different colors
    plt.scatter(df["Date"].loc[df["Voltage (L-L)"] == min_voltage], min_voltage, color='red', s=300, label="Min Voltage")
    plt.scatter(df["Date"].loc[df["Voltage (L-L)"] == max_voltage], max_voltage, color='green', s=300, label="Max Voltage")

    # Add a legend for the main plot
    plt.legend()

    # Add a separate legend for min, max, and mean values
    plt.figtext(0.15, 0.2, f"Min Voltage: {min_voltage:.2f}", color='red')
    plt.figtext(0.15, 0.23, f"Max Voltage: {max_voltage:.2f}", color='green')
    plt.figtext(0.15, 0.26, f"Mean Voltage: {mean_voltage:.2f}", color='blue')

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to be every month
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
