"""This module contains functions for data wrangling."""

import pandas as pd

from eppopynder._utils import _checks

def uniform_taxonomy(taxonomy_data):
    """Create a complete and uniform taxonomy dataframe.

    This function normalizes the taxonomy returned by the EPPO service,
    producing a uniform structure that includes all possible taxonomic
    categories, even when some of them are not present in the original result.

    Args:
        taxonomy_data (pandas.DataFrame): A dataframe containing taxonomy data
            provided by the EPPO service for a given EPPO code.

    Returns:
        pandas.DataFrame: A dataframe where each row represents one of the
        expected taxonomic ranks. Fields corresponding to ranks not present in
        the original taxonomy are filled with `NaN`/`NaT`. The `level` column
        is excluded from the output.

    Examples:
        >>> from eppopynder import Client, TaxonService uniform_taxonomy

        >>> client = Client()

        >>> # Retrieve taxonomy data from the EPPO service.
        >>> taxon_data = client.taxon(
        ...     eppo_codes=["BEMITA"],
        ...     services=[TaxonService.TAXONOMY]
        ... )

        >>> # Create a uniform taxonomy with all ranks.
        >>> taxonomy = uniform_taxonomy(
        ...     taxonomy_data=taxon_data[TaxonService.TAXONOMY])
    """

    _checks._require_type(value=taxonomy_data, expected_type=pd.DataFrame)
    _checks._require_column_names(dataframe=taxonomy_data,
                                  column_names=["queried_eppo_code", "type"])
    _checks._require_not_all_nan(dataframe=taxonomy_data,
                                 column_name="queried_eppo_code")

    taxonomy_types_ = pd.DataFrame({
        "type": [
            "Kingdom",
            "Phylum",
            "Subphylum",
            "Class",
            "Subclass",
            "Order",
            "Suborder",
            "Family",
            "Subfamily",
            "Genus",
            "Species"
        ]
    })

    uniformed_taxonomy_data_ = (
        taxonomy_types_
        .merge(taxonomy_data, on="type", how="left")
        .drop(columns="level", errors="ignore")
    )

    queried_eppo_code_ = \
        uniformed_taxonomy_data_["queried_eppo_code"].dropna().iloc[0]

    uniformed_taxonomy_data_["queried_eppo_code"] = \
        uniformed_taxonomy_data_["queried_eppo_code"] \
            .fillna(queried_eppo_code_)

    return uniformed_taxonomy_data_
