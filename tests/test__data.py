import unittest
import pandas as pd

from eppopynder._utils._data import (_flatten, _transform_taxons,
                                     _transform_references, _merge_batch)
from eppopynder._core._taxons import TaxonsService
from eppopynder._core._references import ReferencesService


class TestData(unittest.TestCase):

    ##############
    # _flatten() #
    ##############

    def test__flatten_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _flatten, nested_data=123)

    def test__flatten_empty(self):
        """Test the behaviour for empty data."""
        self.assertTrue(_flatten(nested_data=list()).empty)
        self.assertTrue(_flatten(nested_data=dict()).empty)

    def test__flatten_sep(self):
        flattened_ = _flatten(nested_data={'a': {'b': 1}})
        self.assertEqual(flattened_.keys()[0], "a_b")
        flattened_ = _flatten(nested_data={'a': {'b': 1}}, separator='.')
        self.assertEqual(flattened_.keys()[0], "a.b")

    def test__flatten_dict1(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                '1': 4,
                '2': 5
            }
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', 'b', 'c', "d_1", "d_2"]
        )

    def test__flatten_dict2(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                '1': 4,
                '2': {
                    '3': 5
                }
            }
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', 'b', 'c', "d_1", "d_2_3"]
        )

    def test__flatten_dict3(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6}
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', "b_x", "b_y", "b_z"]
        )

    def test__flatten_dict4(self):
        """Test the behaviour for flattening a dictionary."""
        flattened_ = _flatten(nested_data={
            'a': 1,
            'b': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6},
                "some text"
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ['a', "b_x", "b_y", "b_z", 'b']
        )

    def test__flatten_list_of_dicts(self):
        """Test the behaviour for flattening a list of dictionaries."""
        flattened_ = _flatten(nested_data=[
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 4, 'b': 5, 'c': 6}
        ])
        self.assertEqual(list(flattened_.keys()), ['a', 'b', 'c'])

    def test__flatten_dict_of_lists1(self):
        """Test the behaviour for flattening a dictionary of lists."""
        flattened_ = _flatten(nested_data={
            'a': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6}
            ],
            'b': [
                {'x': 7, 'y': 8, 'z': 9},
                {'x': 10, 'y': 11, 'z': 12}
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ["parent_key", 'x', 'y', 'z']
        )

    def test__flatten_dict_of_lists2(self):
        """Test the behaviour for flattening a dictionary of lists."""
        flattened_ = _flatten(nested_data={
            'a': [
                {'x': 1, 'y': 2, 'z': 3},
                {'x': 4, 'y': 5, 'z': 6}
            ],
            'b': [
                {'x': 7, 'y': 8, 'z': 9},
                "some text"
            ]
        })
        self.assertEqual(
            list(flattened_.keys()),
            ["parent_key", 'x', 'y', 'z', "atomic_value"]
        )

    #######################
    # _transform_taxons() #
    #######################

    def test__transform_taxons_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _transform_taxons, taxons_data=123)

    def test__transform_taxons_valid(self):
        """Test the behaviour for valid data."""
        data_ = _transform_taxons(taxons_data={
            TaxonsService.LIST: pd.DataFrame({
                "pagination_a": [1, 2, 3],
                "meta_b": [4, 5, 6],
                "other": [7, 8, 9]
            })
        })
        self.assertEqual(
            list(data_[TaxonsService.LIST].keys()),
            ["other"]
        )

    ###########################
    # _transform_references() #
    ###########################

    def test__transform_references_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _transform_references,
                          references_data=123)

    def test__transform_references_valid(self):
        """Test the behaviour for valid data."""
        data_ = _transform_references(references_data={
            ReferencesService.COUNTRIES_STATES: pd.DataFrame({
                "parent_key": [1, 2, 3],
                "other_1": [4, 5, 6],
                "other_2": [7, 8, 9]
            })
        })
        self.assertEqual(
            list(data_[ReferencesService.COUNTRIES_STATES].keys()),
            ["country_iso", "other_1", "other_2"]
        )

    ##################
    # _merge_batch() #
    ##################

    def test__merge_batch_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _merge_batch, datasets=123,
                          parent_column_name="")
        self.assertRaises(TypeError, _merge_batch, datasets=dict(),
                          parent_column_name=123)

    def test__merge_batch_valid(self):
        """Test the behaviour for valid data."""
        data_ = _merge_batch(
            datasets={
                "service1": {
                    'A': pd.DataFrame({}),
                    'B': pd.DataFrame({})
                }
            },
            parent_column_name="parent_name"
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), ["service1"])
        self.assertIsInstance(data_["service1"], pd.DataFrame)
        self.assertEqual(
            list(data_["service1"].keys()),
            ["parent_name"]
        )
