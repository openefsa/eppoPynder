import unittest
from eppoPynder.query_the_whole_eppo import query_the_whole_eppo

class TestQueryTheWholeEPPO(unittest.TestCase):
    
    def test_getting_7_dataframes_are_returned(self):        
        result = query_the_whole_eppo('BEMITA')
        self.assertEqual(len(result), 7)
        
    def test_getting_the_right_names(self):  
        services = ["general", "names", "taxonomy", "categorization", "hosts", "pests", "kingdom"]      
        result = query_the_whole_eppo('BEMITA')
        
        self.assertEqual(list(result.keys()), services)

    def test_missing_token(self):
        # Test when token is None
        with self.assertRaises(ValueError) as context:
            query_the_whole_eppo("BEMITA", token=None)
        self.assertEqual(str(context.exception), "EPPO token is required. Please provide a valid token.")
        
        # Test when token is an empty string
        with self.assertRaises(ValueError) as context:
            query_the_whole_eppo("BEMITA", token="")
        self.assertEqual(str(context.exception), "EPPO token is required. Please provide a valid token.")