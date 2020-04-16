from datetime import datetime
import ast

class Restaurant:
    """
    Authors: Dean, Tony and Hashir.

    Class defining Restaurant object. Holds all relevant information.

    Attributes:
        name - string - name of restaurant
        address - string - street address of restaurant
        coordinates - tuple containing latitude and longitude
        stars - average star rating for a restaurant
        topReviews - multi-element tuple containing single string as review
        hours - dictionairy for hours where key is string of the day of the week
    """

    def __init__(self, name, address=None, coordinates=None, stars=None, 
                    numberOfReviews=None, topReviews=None, hours=None, averageNearbyRating=None):
        self.name = name
        self.address = address[0][0] if address is not None else "unavailable"
        self.coordinates = coordinates[0] if coordinates is not None else (0,0)
        self.stars = stars[0][0] if stars is not None else "unavailable"
        self.numberOfReviews = numberOfReviews[0][0] if numberOfReviews is not None else "unavailable"
        self.topReviews = topReviews[0] if topReviews is not None else ""
        try:
            self.hours = ast.literal_eval(hours[0][0]) if hours is not None else ""
        except ValueError:
            self.hours = None
            print("yikes hours valueerror for " + name)
        self.averageNearbyRating = averageNearbyRating

    def getHours(self):
        """
        Returns the hours for the current day using current system time

        Returns:
            string - hours for the current day

        """

        if not isinstance(self.hours, dict):
            return "Hours unavailable"

        return self.hours.get(datetime.today().strftime('%A'), "Hours unavailable")
