import unittest
import pandas as pd
from eppoPynder.taxonomy_ranked import taxonomy_ranked

class TaxonomyRanked(unittest.TestCase):
    def test_taxonomy_ranked_merge_and_transform(self):
        # Create test input data
        taxonomy = pd.DataFrame({
            'eppocode': ['CODE1'],
            'queried_eppocode': ['BEMITA'],
            'name': ['Test Species']
        })
        
        kingdom = pd.DataFrame({
            'eppocode': ['CODE1'],
            'queried_eppocode': ['BEMITA'],
            'status': ['Animalia']
        })
        
        # Call the function
        result = taxonomy_ranked(taxonomy, kingdom)
        
        # Verify the results
        assert 'rank' in result.columns
        assert result.columns[0] == 'rank'  # Check if rank is first column
        assert result.iloc[0]['rank'] == 'kingdom'
        assert len(result) == 1