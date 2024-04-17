# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:45:37 2024

@author: Amitr
"""

from flask import Flask, render_template

app = Flask(__name__, template_folder='', static_folder='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/images/resources.csv')
def get_csv():
    with open('assets/images/resources.csv', 'r') as file:
        csv_data = file.read()
    return csv_data, 200, {'Content-Type': 'text/csv'}

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
