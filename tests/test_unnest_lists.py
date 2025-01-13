import unittest

from eppoPynder.unnest_lists import unnest_lists

class TestUnnestLists(unittest.TestCase):

    def test_unnest_lists_all_keys_present(self):
        # Test when all keys are present and the lists are non-empty
        input_data = {
            "Major host": ["Host1", "Host2"],
            "Host": ["Host3", "Host4"],
            "Wild/Weed": ["Host5"],
            "Alternate": ["Host6", "Host7"],
            "Experimental": ["Host8"],
            "Doubtful host": [],
            "Non-host": ["Host9"]
        }
        expected_output = [
            "Host1", "Host2", "Host3", "Host4", "Host5", 
            "Host6", "Host7", "Host8", "Host9"
        ]
        result = unnest_lists(input_data)
        self.assertEqual(result, expected_output)

    def test_unnest_lists_some_keys_missing(self):
        # Test when some keys are missing
        input_data = {
            "Major host": ["Host1", "Host2"],
            "Host": ["Host3"]
        }
        expected_output = ["Host1", "Host2", "Host3"]
        result = unnest_lists(input_data)
        self.assertEqual(result, expected_output)

    def test_unnest_lists_non_dict_input(self):
        # Test when the input is not a dictionary (edge case)
        input_data = ["Some", "List"]
        expected_output = ["Some", "List"]
        result = unnest_lists(input_data)
        self.assertEqual(result, expected_output)

    def test_unnest_lists_with_empty_lists(self):
        # Test when input has empty lists for some of the keys
        input_data = {
            "Major host": ["Host1"],
            "Host": [],
            "Wild/Weed": [],
            "Alternate": [],
            "Experimental": [],
            "Doubtful host": [],
            "Non-host": ["Host2"]
        }
        expected_output = ["Host1", "Host2"]
        result = unnest_lists(input_data)
        self.assertEqual(result, expected_output)

    def test_unnest_lists_with_none_values(self):
        # Test when the input has None for some values of the lists
        input_data = {
            "Major host": None,
            "Host": ["Host1"],
            "Wild/Weed": None,
            "Alternate": None,
            "Experimental": ["Host2"],
            "Doubtful host": None,
            "Non-host": ["Host3"]
        }
        expected_output = ["Host1", "Host2", "Host3"]
        result = unnest_lists(input_data)
        self.assertEqual(result, expected_output)