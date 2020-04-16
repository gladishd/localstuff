import unittest 
from datasource import * 

class DataSourceTester(unittest.TestCase):
    def setUp(self):
        self.ds = DataSource()

    def tearDown(self):
        pass

    def test_not_list(self):
        list_of_nums = 12
        self.assertEqual(self.ds.getAverageStarRating(list_of_nums), "Input not list")

    def test_invalid_list_character(self):
        list_of_nums = [('a',),(4.0,),(6.0,)]
        self.assertEqual(self.ds.getAverageStarRating(list_of_nums), "Invalid input")

    def test_response(self):
        list_of_nums = [(8.0,),(4.0,),(6.0,)]
        self.assertEqual(self.ds.getAverageStarRating(list_of_nums), 6)
        
    def test_empty_list(self):
        empty_list = []
        self.assertEqual(self.ds.getAverageStarRating(empty_list), 0)
        
    def test_multiple_floats(self):
        list_of_nums = [(2.0, 4.0),(3.5,),(5.0,)]
        self.assertEqual(self.ds.getAverageStarRating(list_of_nums), 3.5)
         
if __name__ == '__main__':
    unittest.main()
