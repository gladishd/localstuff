import psycopg2
from numpy import arange
from statistics import mean
from backend.restaurant import Restaurant

class DataSource:
    """
    Authors: Dean, Tony and Hashir.

    DataSource executes all of the queries on the database.

    It also formats the data in preparation to send it back
    to the frontend, and in our case we format the data into 
    restaurant objects for use in the front end.

    Starter code authored by Amy Csizmar Dalal.
    """

    def searchRestaurantsByName(self, name):
        """
        Returns a list of all restaurants which include a given name string in the name.
        If name is an empty string, will return all restaurants.

        Parameters:
            name (string): input name to search for, case-insensitive
        Returns:
            list: a list of all restaurant names that include the string
        """

        if name == "":
            name = "%"
        else:
            name = "%" + name + "%" # using wildcard SQL search to get similar names

        query = "SELECT DISTINCT name FROM mississauga WHERE name ILIKE %s"
        return self.runQuery(query, (name,))

    def getRestaurantsByMinimumStars(self, stars):
        """
        Returns a list of all restaurants which have at least certain number of stars.

        Parameters:
            stars (int): the minimum number of stars
        Returns:
            list: a list of all restaurant names with a certain number of stars.
        """

        query = "SELECT DISTINCT name FROM mississauga WHERE stars >= %s"
        return self.runQuery(query, (stars,))

    def searchRestaurantsByNameAndMinimumStars(self, name, stars):
        """
        Returns a list of all restaurants which include a given string in the name
        and have at least certain number of stars.
        If name is an empty string, will return all restaurants.
        A combined function for greater efficiency with fewer SQL calls.

        Parameters:
            name (string): input name to search for, case-insensitive
            stars (int): the minimum number of stars
        Returns:
            list: a list of all restaurant names that include the string and with a certain number of stars.
        """

        if name == "":
            name = "%"
        else:
            name = "%" + name + "%" # using wildcard SQL search to get similar names

        query = "SELECT DISTINCT name FROM mississauga WHERE name ILIKE %s AND stars >= %s"
        return self.runQuery(query, (name, stars,))

    def getRestaurantAddress(self, name):
        """
        Retrieves address of given restaurant name

        Parameters:
            name - name of restaurant
        Returns:
            a tuple containing the address as a string
        """

        query = "SELECT DISTINCT address from mississauga where name = %s"
        return self.runQuery(query, (name,))

    def getAverageStarRating(self, listOfStars):
        """
        For use with getStarsByLocation to determine average star rating of a region.

        Parameters:
            listOfStars - list of stars returned by getStarsByLocation
        Returns:
            the average star rating of the list
        """

        if not isinstance(listOfStars, list):
            return "Input not list"

        totalStarCount = 0
        for row in listOfStars:
            # row contains one float as a tuple
            if not isinstance(row[0], float):
                return "Invalid input"
            totalStarCount += row[0]
        return round(totalStarCount/len(listOfStars), 1) if len(listOfStars) else 0.0

    def getStarsByLocation(self, nameOfRestaurant, radius):
        """
        Retrieves a list of Stars of a given square range around a restaurant

        Parameters:
            nameOfResturants - name of restaurants
            radius - the radius in miles around the restaurant
        Returns:
            a collection of stars of given restaurant names
        """

        location = self.getLocation(nameOfRestaurant)
        query = "SELECT DISTINCT stars from mississauga where longitude between %s and %s AND latitude between %s and %s"
        return self.runQuery(query, (str(location[0]-radius/69), str(location[0]+radius/69), str(location[1]-radius/69), str(location[1]+radius/69),))

    def getRestaurantsNearby(self, nameOfRestaurant, radius):
        """
        Retrieves a list of all restaurants which are located within a square
        region around another restaurant.

        Parameters:
            nameOfRestaurant - name of restaurant to find other locations around
            radius - region in miles around the restaurant
        Returns:
            a list of restaurant names
        """

        location = self.getLocation(nameOfRestaurant)
        query = "SELECT DISTINCT name FROM mississauga where longitude %s and %s AND latitude between %s and %s"
        return self.runQuery(query, (str(location[0]-radius/69), str(location[0]+radius/69), str(location[1]-radius/69), str(location[1]+radius/69),))

    def getLocation(self, nameOfRestaurant):
        """
        Retrieves the latitude and longitude of a restuarant

        Parameters:
            nameOfRestaurant - name of restaurant
        Returns:
            a list containing the latitude and longitude of the restaurant
        Raises:
            an exception if the query fails
        """
        # TODO: figure out fetchone() alternative

        try:
            cursor = self.connection.cursor()
            query = "SELECT DISTINCT longitude, latitude from mississauga where name ILIKE %s"
            cursor.execute(query, (nameOfRestaurant, ))
            return cursor.fetchone()
        except Exception as e:
    	    print ("Something went wrong when executing the query: ", e)
    	    return None

    def getTop5Reviews(self, nameOfRestaurant):
        """
        Retrieves the top review selected by most useful review for the specified restaurant

        Parameters:
            name - The full name of the restaurant.
        Returns:
            a list of the text of the top five reviews
        """

        query = "SELECT text FROM mississauga WHERE name ILIKE %s ORDER BY useful DESC LIMIT 5"
        return self.runQuery(query, (nameOfRestaurant,))

    def getNumberOfReviews(self, nameOfRestaurant):
        """
        Retrieves the the number of Yelp reviews submitted for the specified restaurant

        Parameters:
            name - The full name of the restaurant.
        Returns:
            a tuple containing the number of reviews as an integer
        """

        query = "SELECT COUNT(name) FROM mississauga WHERE name ILIKE %s"
        return self.runQuery(query, (nameOfRestaurant,))

    def getStarRating(self, nameOfRestaurant):
        """
        Retrieves the star rating of a restaurant out of a mazimum of 5

        Parameters:
            name - The full name of the restaurant.
        Returns:
            a tuple containing the address as a string
        """

        query = "SELECT MAX(DISTINCT stars) FROM mississauga WHERE name ILIKE %s"
        return self.runQuery(query, (nameOfRestaurant,))

    def getRestaurantTimings(self, nameOfRestaurant):
        """
        Retrieves the hours a restaurant is open

        Parameters:
            name - The full name of the restaurant.
        Returns:
            a tuple containing as a string JSON containing hours for each day of the week
        """

        query = "SELECT DISTINCT hours FROM mississauga WHERE name ILIKE %s LIMIT 1"
        return self.runQuery(query, (nameOfRestaurant,))

    def runQuery(self, queryText, variables):
        """
        Helper function to run SQL query on database

        Parameters:
            queryText - string of SQL query
        Returns:
            a list containing the results of the query
        Raises:
            an exception if the query fails
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(queryText, variables)
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def generateRestaurantObjects(self, listOfRestaurantNames):
        """
            Genereates and returns a list of Restaurant object using a list of restaurant names
            Parameters:
                listOfRestaurantNames - string containing list of restaurant names to make objects of
            Returns:
                list of Restaurant objects 
        """

        restaurants = []

        for name in listOfRestaurantNames:
            name = name[0] # since backend return value is a single value in a tuple
            restaurant = Restaurant(name=name,
                                    address=self.getRestaurantAddress(name),
                                    stars=self.getStarRating(name),
                                    numberOfReviews=self.getNumberOfReviews(name),
                                    topReviews=self.getTop5Reviews(name),
                                    hours=self.getRestaurantTimings(name),
                                    averageNearbyRating=self.getAverageStarRating(self.getStarsByLocation(name, 3)))
            restaurants.append(restaurant)

        return restaurants
    
    def __init__(self):
        user = 'safdarh'
        password = 'python986lion'
        try:
            self.connection = psycopg2.connect(database=user, user=user, password=password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()


def main():
    # testing code
    ds = DataSource()
    location = ds.getRestaurantAddress("Popular Pizza")
    print(location)
    restaurant_info = ds.searchRestaurantsByName("Pizza")
    print(restaurant_info)

# main()
