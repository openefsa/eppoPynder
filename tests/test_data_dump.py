import unittest

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

    def test_missing_token(self):
        # Test when token is None
        with self.assertRaises(ValueError) as context:
            data_dump(["BEMITA"], token=None)
        self.assertEqual(str(context.exception), "EPPO token is required. Please provide a valid token.")
        
        # Test when token is an empty string
        with self.assertRaises(ValueError) as context:
            data_dump(["BEMITA"], token="")
        self.assertEqual(str(context.exception), "EPPO token is required. Please provide a valid token.")
