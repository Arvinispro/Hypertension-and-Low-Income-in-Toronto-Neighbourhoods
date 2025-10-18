"""CSCA08: Assignment 3: Hypertension and Low Income

Starter code for tests to test function get_bigger_neighbourhood in
a3.py.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) Jacqueline Smith, David Liu, and Anya Tafliovich

"""

import copy
import unittest
from a3 import get_bigger_neighbourhood as gbn
from a3 import SAMPLE_DATA


class TestGetBiggerNeighbourhood(unittest.TestCase):
    """Test the function get_bigger_neighbourhood."""

    def test_first_bigger(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when its population is strictly greater than the
        population of the second neighbourhood.

        """
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Rexdale-Kipling', 'Elms-Old Rexdale')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_second_bigger(self):
        """Test that get_bigger_neighbourhood correctly returns the second
        neighbourhood when its population is strictly greater than the
        population of the first neighbourhood.
        """
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Elms-Old Rexdale', 'Rexdale-Kipling')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg) 
        
    def test_equal_popu(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when its population is equal to the
        population of the second neighbourhood.
        """
        sample_data_copy = copy.deepcopy(THIRD_DATA)
        expected = 'West Humber-Clairville'
        actual = gbn(THIRD_DATA, 'West Humber-Clairville', 
                     'Mount Olive-Silverstone-Jamestown')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)    
        
    def test_first_not_in_city(self):
        """Test that get_bigger_neighbourhood correctly returns the second
        neighbourhood when the first neighbourhood is not in the city
        """
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'New York', 'Rexdale-Kipling')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)       
        
    def test_second_not_in_city(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when the second neighbourhood is not in the city
        """
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Rexdale-Kipling'
        actual = gbn(SAMPLE_DATA, 'Rexdale-Kipling', 'New York')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)    
        
    def test_both_not_in_city(self):
        """Test that get_bigger_neighbourhood correctly returns the first
        neighbourhood when the both neighbourhoods are not in the city
        """
        sample_data_copy = copy.deepcopy(SAMPLE_DATA)
        expected = 'Toronto'
        actual = gbn(SAMPLE_DATA, 'Toronto', 'New York')
        msg = message(sample_data_copy, expected, actual)
        self.assertEqual(actual, expected, msg)
        
def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ("When we called get_most_published_authors(" + str(test_case) +
            ") we expected " + str(expected) +
            ", but got " + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)
