import unittest
import pandas as pd

from eppopynder.data_wrangling import uniform_taxonomy


class TestDataWrangling(unittest.TestCase):

    ######################
    # uniform_taxonomy() #
    ######################

    def test_uniform_taxonomy_types(self):
        """Test if the parameters are of the correct types."""
        self.assertRaises(TypeError, uniform_taxonomy, taxonomy_data=123)
        self.assertRaises(ValueError, uniform_taxonomy,
                          taxonomy_data=pd.DataFrame())
        self.assertRaises(ValueError, uniform_taxonomy,
                          taxonomy_data=pd.DataFrame({
                              "queried_eppo_code": [None],
                              "type": ["type_a"]
                          }))

    def test_output(self):
        """Test the output for correct parameters."""
        taxonomy_ = pd.DataFrame({
            "queried_eppo_code": ['A', 'A', 'A'],
            "eppocode": ['D', 'E', 'F'],
            "prefname": ['G', 'H', 'I'],
            "level": ['1', '2', '3'],
            "type": ['Kingdom', 'Class', 'Order'],
            "queried_url": ['M', 'N', 'O'],
            "queried_on": ['P', 'Q', 'R'],
        })
        self.assertIsInstance(uniform_taxonomy(taxonomy_data=taxonomy_),
                              pd.DataFrame)
