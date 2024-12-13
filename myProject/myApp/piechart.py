# Import Libraries
import pandas as pd
import plotly.express as px
from datetime import timedelta
import os

# Load and Process Data
def load_and_process_data(file_path):
    data = pd.read_csv(file_path)
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    data = data.dropna(subset=['Time'])
    data['Date'] = data['Time'].dt.date
    data['Time_Only'] = data['Time'].dt.time
    return data

# Visualization Functions
def plot_1_hour(data, time):
    subset = data[data['Time'] == time]
    if subset.empty:
        return None
    consumption = subset.iloc[0, 2:-2]
    fig = px.pie(values=consumption, names=consumption.index, title=f"Electricity Consumption at {time}")
    return fig.to_html()

def plot_5_hours(data, start_time, end_time):
    subset = data[(data['Time'] >= start_time) & (data['Time'] < end_time)]
    if subset.empty:
        return None
    subset = subset.melt(id_vars='Time', var_name='Appliance', value_name='Consumption')
    fig = px.bar(subset, x='Time', y='Consumption', color='Appliance', title=f"Consumption from {start_time} to {end_time}")
    return fig.to_html()

def plot_24_hours(data, start_time, end_time):
    subset = data[(data['Time'] >= start_time) & (data['Time'] < end_time)]
    if subset.empty:
        return None
    total_consumption = subset.iloc[:, 2:-2].sum()
    fig = px.pie(values=total_consumption, names=total_consumption.index, title="24-Hour Total Appliance Consumption")
    return fig.to_html()
