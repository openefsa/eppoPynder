import unittest
import pandas as pd
import numpy as np

from eppoPynder.taxonomy_ranked import taxonomy_ranked
from eppoPynder.query_the_eppo_for_service import query_the_eppo_for_service

class TestTaxonomyRanked(unittest.TestCase):

    def test_output_is_dataframe(self):
        # Get kingdom and taxonomy data
        kingdom = query_the_eppo_for_service("BEMITA", service="kingdom")
        taxonomy = query_the_eppo_for_service("BEMITA", service="taxonomy")
        
        # Debugging: Check data types of the inputs
        print(f"taxonomy type: {type(taxonomy)}")
        print(f"kingdom type: {type(kingdom)}")
        print(f"taxonomy dtypes:\n{taxonomy.dtypes}")

        # Ensure taxonomy is a DataFrame and kingdom is valid
        result = taxonomy_ranked(taxonomy, kingdom)
        
        # Check if the result is a DataFrame
        self.assertTrue(isinstance(result, pd.DataFrame), "Result is not a dataframe")

    def setUp(self):
        # Sample taxonomy DataFrame
        self.taxonomy_data = {
            'eppocode': ['BEMITA', 'BEMITA', 'SOMECODE'],
            'queriedEppocode': ['BEMITA', 'BEMITA', 'SOMECODE'],
            'taxonRank': ['species', 'genus', 'family']
        }
        self.taxonomy = pd.DataFrame(self.taxonomy_data)

        # Sample kingdom DataFrame
        self.kingdom_data = {
            'eppocode': ['BEMITA', 'SOMECODE'],
            'queriedEppocode': ['BEMITA', 'SOMECODE'],
            'rank': ['active', 'inactive']
        }
        self.kingdom = pd.DataFrame(self.kingdom_data)

    def test_empty_kingdom_dataframe(self):
        # Test case where kingdom DataFrame is empty
        empty_kingdom = pd.DataFrame(columns=['eppocode', 'queriedEppocode', 'status'])
        result = pd.merge(self.taxonomy, empty_kingdom[["eppocode", "queriedEppocode", "status"]], how='left', on=["eppocode", "queriedEppocode"])

        # Check if 'rank' is NaN when there is no match in kingdom data
        result = result.rename(columns={'status': 'rank'})
        result.insert(0, "rank", result.pop("rank"))
        result["rank"] = np.where(result["rank"].notnull(), "kingdom", pd.NA)

        self.assertTrue(result['rank'].isna().all(), "All values in 'rank' should be NaN when kingdom data is empty.")