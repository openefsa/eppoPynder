import unittest
from unittest.mock import patch
import pandas as pd

from eppoPynder.query_the_eppo_for_service import query_the_eppo_for_service

class TestQueryTheEPPOForService(unittest.TestCase):

    def test_if_code_is_passed_dataframe_is_returned(self):
        result = query_the_eppo_for_service("BEMITA")
        self.assertTrue(isinstance(result, pd.DataFrame))

    @patch('eppoPynder.query_the_eppo_for_service')
    def test_if_wrong_service_is_requested_standard_df_returned(self, mock_query):
        mock_query.return_value = pd.DataFrame(columns=['col1', 'col2', 'col3'])
        result = query_the_eppo_for_service("BEMITA", service="wrongservice")
        self.assertEqual(result.shape[1], 3)

    def test_default_token_assignment(self):
        with patch('eppoPynder.query_the_eppo_for_service.api_query') as mock_api:
            # Configure mock to return an empty DataFrame
            mock_api.return_value = pd.DataFrame()
            
            # Call function without a token
            result = query_the_eppo_for_service("BEMITA", token=None)
            
            # Get the call arguments
            call_args = mock_api.call_args
            
            # Extract the queried_url from the kwargs
            queried_url = call_args.kwargs['queried_url']
            
            # Verify that default_token was used in the URL
            self.assertIn('authtoken=default_token', queried_url)
