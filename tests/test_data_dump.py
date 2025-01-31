import unittest
from unittest.mock import patch
import pandas as pd
from eppoPynder.data_dump import data_dump


class DataDumpEppo(unittest.TestCase):

    def test_data_dump(self):
        # Call the function being tested
        result = data_dump(["BEMITA", "LEUCSC"])

        # Ensure the dictionary contains the expected keys
        services = ["general", "names", "taxonomy", "categorization", 
                    "hosts", "pests", "kingdom"]

        self.assertTrue(
            set(services).issubset(result.keys()),
            "The keys in the dictionary do not match the expected services.")

    def test_input_type_validation(self):
        with self.assertRaises(AssertionError) as context:
            data_dump("not_a_list")
        self.assertEqual(str(context.exception), "Input must be a list!")

        with self.assertRaises(AssertionError) as context:
            data_dump([])
        self.assertEqual(str(context.exception), "Input list cannot be empty!")

        with self.assertRaises(AssertionError) as context:
            data_dump(["BEMITA", 123])
        self.assertEqual(str(context.exception), "All codes must be strings!")

    def test_non_string_token_raises_assertion_error(self):
        with self.assertRaisesRegex(AssertionError, "token must be a string!"):
            data_dump(["BEMITA"], token=123)

    def test_default_token_assignment(self):
        with patch('eppoPynder.data_dump.query_the_eppo_for_service') as mock_query:
            # Configure mock to return a DataFrame with required columns
            mock_query.return_value = pd.DataFrame({'queried_eppocode': ['BEMITA']})
            
            # Call function without a token
            result = data_dump(["BEMITA"], token=None)
            
            # Get the first call to verify token value
            first_call = mock_query.call_args_list[0]
            
            # Verify that default_token was used
            self.assertEqual(first_call.kwargs['token'], 'default_token')
