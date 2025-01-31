import unittest
from unittest.mock import patch
import pandas as pd
from eppoPynder.query_the_whole_eppo import query_the_whole_eppo

class TestQueryTheWholeEPPO(unittest.TestCase):
    
    def test_getting_7_dataframes_are_returned(self):        
        result = query_the_whole_eppo('BEMITA')
        self.assertEqual(len(result), 7)
        
    def test_getting_the_right_names(self):  
        services = ["general", "names", "taxonomy", "categorization", "hosts", "pests", "kingdom"]      
        result = query_the_whole_eppo('BEMITA')
        
        self.assertEqual(list(result.keys()), services)

    def test_non_string_token_raises_assertion_error(self):
        with self.assertRaisesRegex(AssertionError, "token must be a string!"):
            query_the_whole_eppo("BEMITA", token=123)

    def test_default_token_assignment(self):
        # Using the full import path for the mock
        with patch('eppoPynder.query_the_whole_eppo.query_the_eppo_for_service') as mock_query:
            # Configure mock to return an empty DataFrame
            mock_query.return_value = pd.DataFrame()
            
            # Call function without a token
            result = query_the_whole_eppo("BEMITA", token=None)
            
            # Get the first call to verify token value
            first_call = mock_query.call_args_list[0]
            
            # Verify that default_token was used
            self.assertEqual(first_call.kwargs['token'], 'default_token')

                