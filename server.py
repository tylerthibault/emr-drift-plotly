
from flask import Flask, render_template, redirect, session, request, jsonify
import helper
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = "shhhhhhhhhhhhhhhhhhhhhhh"

app.temp_storage = {}

@app.route("/")
def index():
    if 'pns' not in app.temp_storage:
        print("setting pns")
        app.temp_storage['pns'] = []

    context = {
        'pns': app.temp_storage['pns']
    }
    return render_template('index.html', **context)

@app.route('/get_data')
def get_data():
    pn_list = helper.get_pn(30)

    datapoints = []

    for num in pn_list:
        for x in range(30):
            datapoints.append(
                {
                    'date' : helper.get_dates(1),
                    'value' : helper.get_values(1),
                    'pn' : pn_list[x],
                }
            )

    return render_template('/get_data.html', datapoints = datapoints)

@app.route('/process', methods=['GET', 'POST'])
@app.route('/process/<pn>', methods=['GET'])
def process(pn=-1):
    if pn != -1:
        data = {'pn': pn}
    elif request.method == "GET":
        data = {'pn':app.temp_storage['pns'][-1]}
    else:
        data = {**request.form}
    pn = data['pn']
    part_list = helper.search(data['pn'])

    plot_fig = helper.get_graph(part_list)

    if 'remember' in data:
        session['remember'] = pn
    else:
        if 'remember' in session:
            del session['remember']

    
    if pn not in app.temp_storage['pns']:
        app.temp_storage['pns'].append(pn)


    app.temp_storage['part_list'] = part_list
    app.temp_storage['plot_fig'] = plot_fig
    return redirect('/display')

@app.post('/bulk/process')
def bulk_upload():
    data = {**request.form}
    part_numbers_str = data['part_numbers']
    # Step 1: Clean and split the part numbers string
    part_numbers_list = [pn.strip() for pn in part_numbers_str.splitlines() if pn.strip()]

    # Step 2: Initialize a list to store the HTML representations of the graphs
    graphs_html = []

    # Step 3: Loop through each part number, get the data, and generate the graph
    for pn in part_numbers_list:
        # Search for the data using the helper function
        part_list = helper.search(pn)

        # Generate the graph using the helper function
        plot_html = helper.get_graph(part_list)

        # Append the HTML representation of the graph to the list
        graphs_html.append(plot_html)
    
    app.temp_storage['graphs_html'] = graphs_html
    return redirect("/display/bulk")

@app.route("/display/bulk")
def display_bulk():
    context = {
        'graphs_html': app.temp_storage['graphs_html']
    }
    return render_template('display_bulk.html', **context)

@app.route('/display')
def display():
    if not app.temp_storage:
        return redirect('/process')
    

    context = {
        'part_list': app.temp_storage['part_list'],
        'plot_fig': app.temp_storage['plot_fig'],
        'pns': app.temp_storage['pns'],

    }
    return render_template('display.html', **context)

@app.route('/clear/pns')
def clear_pns():
    if 'pns' in app.temp_storage:
        del app.temp_storage['pns']
    return redirect('/')

# keep this at the bottom of this file!!
if __name__=="__main__":
    app.run(debug=True)