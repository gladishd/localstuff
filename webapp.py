import flask
from flask import render_template, request, redirect
import json
import sys
from datetime import datetime
from backend.datasource import DataSource


app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
datasource = DataSource()

@app.route('/')
def home():
    """
    Renders the home page of Restaurant Reviews in Mississauga.
    Audience: all

    RETURNS:
        render Main_Page.html
    """
    return render_template('Main_Page.html')

@app.route('/data')
def data_page():
    """
    Renders the "About Data" page that includes metadata and description of the
    entire dataset. There are also some example data on this page.
    Audience: all

    RETURNS:
        render Data_Page.html
    """

    return render_template('Data_Page.html')

@app.route('/advanced_search')
def advanced_search():
    """
    Renders the advanced search page, a page with only search functionality.

    RETURNS:
        render Advanced_Search.html
    """

    return render_template('Advanced_Search.html')

@app.route('/results', methods = ['POST'])
def results():
    """
    Renders the results page with new info.
    Audience: all

    RETURNS:
        render results.html
    """

    queryName = request.form['query']
    queryStars = request.form['stars']
    
    datasource = DataSource()
    listOfRestaurantNames = datasource.searchRestaurantsByNameAndMinimumStars(queryName, queryStars)
    restaurants = datasource.generateRestaurantObjects(listOfRestaurantNames[:15])

    return render_template('results.html', restaurants=restaurants)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
