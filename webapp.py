import flask
from flask import render_template, request, redirect
import json
import sys
from datetime import datetime
import sys
sys.path.append('../backend/')
from datasource import *
from restaurant import *


app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route('/')
def home():
    '''
    Renders the home page of the entire project about Airbnb in NYC.
    Audience: all

    PARAMETERS:
        None

    RETURNS:
        render Main_Page.html
    '''
    # return render_template('Main_Page.html')
    return render_template('index.html')

# @app.route('/data')
# def data_Page():
#     '''
#     Renders the "About Data" page that includes metadata and description of the
#     entire dataset. There are also some example data on this page.
#     Audience: all
#
#     PARAMETERS:
#         None
#
#     RETURNS:
#         render Data_Page.html
#     '''
#     return render_template('Data_Page.html')

@app.route('/results', methods = ['POST'])
def results():
    queryName = request.form['query']
    queryStars = request.form['stars']
    datasource = DataSource()
    listOfRestaurantNames = set(datasource.searchRestaurantsByName(queryName)).intersection(datasource.getRestaurantsByMinimumStars(queryStars))
    restaurants = []

    for name in listOfRestaurantNames:
        name = name[0] # since backend return value is a single value in a tuple
        restaurant = Restaurant(name=name,
                                address=datasource.getRestaurantAddress(name),
                                coordinates=datasource.getLocation(name),
                                stars=datasource.getStarRating(name),
                                topReviews=datasource.getTop5Reviews(name),
                                hours=datasource.getRestaurantTimings(name))
        restaurants.append(restaurant)

    return render_template('results.html', restaurants=restaurants[:15])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
