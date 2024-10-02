from flask import Flask, render_template, redirect, session, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = "shhhhhhhhhhhhhhhhhhhhhhh"


@app.route('/')
def index():
    x = get_dates()
    y = get_values().tolist()

    # Convert dates to a numerical form to use with polyfit
    x_numeric = np.arange(len(x))

    # Calculate the slope and intercept for the best-fit line
    slope, intercept = np.polyfit(x_numeric, y, 1)

    # Generate the y-values for the best-fit line using the calculated slope and intercept
    y_fit = (slope * x_numeric + intercept).tolist()

    # Pass x, y, and y_fit to the template
    return render_template('/index.html', dates=x, values=y, y_fit=y_fit, slope=slope, intercept=intercept)

@app.route('/millivolts')
def millivolts():
    # Define the Full Scale (FS) value
    FS = 5000  # example: Full Scale is 5000 millivolts

    # Get the original y values in millivolts
    y_mV = get_values().tolist()
    
    y_mV[1] = 3000
    y_mV[5] = -3000


    # Convert y values to %FS
    y_percentage_fs = [(value / FS) * 100 for value in y_mV]

    # Get the x values (dates)
    x = get_dates()  # Already a list of strings

    # Convert to a numeric form for calculating the linear fit
    x_numeric = np.arange(len(x))

    # Calculate the slope and intercept for the best-fit line in terms of %FS
    slope, intercept = np.polyfit(x_numeric, y_percentage_fs, 1)

    # Generate the y-values for the best-fit line using the calculated slope and intercept
    y_fit = (slope * x_numeric + intercept).tolist()

    # Pass x, y_percentage_fs, and y_fit to the template
    return render_template('/millivolts.html', dates=x, values=y_percentage_fs, y_fit=y_fit, slope=slope, intercept=intercept)

@app.route('/millivolts/2')
def millivolts2():
    x = get_dates()
    y = get_values().tolist()

    # Calculate initial slope and intercept for the entire data set
    x_numeric = np.arange(len(x))
    slope, intercept = np.polyfit(x_numeric, y, 1)
    y_fit = (slope * x_numeric + intercept).tolist()

    return render_template('/millivolts2.html', dates=x, values=y, y_fit=y_fit, slope=slope, intercept=intercept)


@app.route('/process_selection', methods=['POST'])
def process_selection():
    data = request.get_json()
    selected_dates = data['dates']
    selected_values = data['values']
    tolerance = data['tolerance']

    # Convert selected dates to numeric indices for calculation
    x_numeric = np.arange(len(selected_dates))

    # Calculate the slope and intercept for the selected range
    slope, intercept = np.polyfit(x_numeric, selected_values, 1)

    # Generate new y-values for the best-fit line using the calculated slope and intercept
    y_fit = (slope * x_numeric + intercept).tolist()

    # Check if the selected range meets the tolerance
    min_value = min(selected_values)
    max_value = max(selected_values)
    range_value = max_value - min_value
    tolerance_status = "PASS" if range_value <= tolerance else "FAIL"

    return jsonify({
        'slope': slope,
        'y_fit': y_fit,
        'tolerance_status': tolerance_status
    })


def get_values():
    return np.random.randint(50, 150, size=30)

def get_dates():
    dates = pd.date_range(start=pd.Timestamp.now(), periods=30, freq='D')
    return dates.strftime('%Y-%m-%d').tolist()

# keep this at the bottom of this file!!
if __name__=="__main__":
    app.run(debug=True)