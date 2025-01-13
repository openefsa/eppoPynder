import unittest
from unittest.mock import patch, MagicMock 
import pandas as pd
import requests
from datetime import date
from eppoPynder.api_query import api_query

class TestApiQuery(unittest.TestCase):

    def test_if_wrong_service_is_requested_standard_df_returned(self): 
        """Test successful API response""" 
        result = api_query("BEMITA", "https://data.eppo.int/api/rest/1.0/taxon/BEMITA?authtoken=token")
        self.assertIn('queried_url', result.columns)
        self.assertEqual(result.iloc[0,0], 'BEMITA')

    @patch('builtins.print')
    @patch('requests.get')
    def test_missing_schema_print(self, mock_get, mock_print):
        mock_get.side_effect = requests.exceptions.InvalidURL()
        api_query("BEMITA", "https://data.eppo.int/api/rest/1.0/taxon/BEMITA?authtoken=token ")
        mock_print.assert_called_once_with('')