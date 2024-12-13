# piechart.py
import pandas as pd
import plotly.express as px
import os

# Load and Process Data
def load_and_process_data(file_path):
    # Load dataset
    data = pd.read_csv(file_path)
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    data['Date'] = data['Time'].dt.date
    data['Time_Only'] = data['Time'].dt.time
    return data

# Generate Graph for 1 Hour
def plot_1_hour(data, time):
    subset = data[data['Time'] == time]
    if subset.empty:
        return None
    consumption = subset.iloc[0, 2:-2]
    fig = px.pie(values=consumption, names=consumption.index, title=f"Electricity Consumption at {time}")
    return fig.to_html()
