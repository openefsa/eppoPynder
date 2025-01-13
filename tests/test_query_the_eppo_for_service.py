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

    def test_missing_token(self):
        # Test when token is None
        with self.assertRaises(ValueError) as context:
            query_the_eppo_for_service("BEMITA", token=None)
        self.assertEqual(str(context.exception), "EPPO token is required. Please provide a valid token.")
        
        # Test when token is an empty string
        with self.assertRaises(ValueError) as context:
            query_the_eppo_for_service("BEMITA", token="")
        self.assertEqual(str(context.exception), "EPPO token is required. Please provide a valid token.")