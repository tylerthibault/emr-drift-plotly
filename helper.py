import string
import random
import pandas as pd
import numpy as np
from data import data
import plotly.graph_objects as go
import datetime


def get_values(quantity):
    return random.randint(50, 150)

def get_dates(quantity):
    # Generate a range of dates over the next 7 days
    start_date = pd.Timestamp.now()
    end_date = start_date + pd.Timedelta(days=6)
    
    # Create a list to hold the generated timestamps
    datetime_list = []

    for _ in range(quantity):
        # Randomly select a day from the 7-day range
        random_date = pd.Timestamp(random.choice(pd.date_range(start=start_date, end=end_date, freq='D')))
        
        # Generate random hour and minute
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)

        # Combine day, hour, and minute into a single timestamp
        random_timestamp = random_date + pd.Timedelta(hours=random_hour, minutes=random_minute)
        
        # Append to the datetime list
        datetime_list.append(random_timestamp)

    # Convert datetimes to string format including hours and minutes
    return [date.strftime('%Y-%m-%d %H:%M') for date in datetime_list]

def get_pn(quantity, length=10, prefix='', suffix=''):
    part_numbers = []
    for _ in range(quantity):
        random_part = ''.join(random.choices('0123456789', k=length))
        part_number = f"{prefix}{random_part}{suffix}"
        part_numbers.append(part_number)
    return part_numbers

def search(pn=123):
    # Filter records with the given part number
    results = [record for record in data if record['pn'] == pn]
    
    # Convert date strings (including time) to datetime objects and sort the results
    sorted_results = sorted(results, key=lambda x: datetime.datetime.strptime(x['date'][0], '%Y-%m-%d %H:%M'))
    
    return sorted_results

def get_graph(data_list):
    # Extracting data from the list
    dates = [entry['date'][0] for entry in data_list]  # Extracting date from each entry
    values = [entry['value'] for entry in data_list]   # Extracting value from each entry
    pn = data_list[0]['pn'] if data_list else "N/A"    # Assuming all have the same pn, get it from the first entry

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name=f'Part Number: {pn}'))
    fig.update_layout(
        title=f'Part Number: {pn} Over Time',
        xaxis_title='Date',
        yaxis_title='Value',
        template='plotly_white'
    )

    # Convert Plotly figure to an HTML div string
    plot_html = fig.to_html(full_html=False)
    return plot_html
