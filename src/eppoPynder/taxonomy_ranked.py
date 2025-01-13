import numpy as np
import pandas as pd

def taxonomy_ranked(taxonomy, kingdom):
    """
    Merge taxonomy and kingdom information into a single dataframe.
    
    Parameters
    ----------
    taxonomy : pd.DataFrame
        A pandas dataframe containing taxonomy data about the queried EPPO code.

    kingdom : pd.DataFrame
        A pandas dataframe containing kingdom data about the queried EPPO code.
    
    Returns
    -------
    taxonomy_ranked_ : pd.DataFrame
        A pandas dataframe containing taxonomy and kingdom information about the queried EPPO code.

    Examples
    --------
    # Get taxonomy and kingdom data about Bemisia tabaci:
    taxonomy = query_the_eppo_for_service(queried_eppocode="BEMITA", service="taxonomy")
    kingdom = query_the_eppo_for_service(queried_eppocode="BEMITA", service="kingdom")

    # Merge taxonomy and kingdom information about Bemisia tabaci into a single dataframe:
    taxonomy_ranked(taxonomy, kingdom)
    """
    taxonomy_ranked_ = pd.merge(taxonomy, kingdom[["eppocode", "queried_eppocode", "status"]], how='left', on=["eppocode", "queried_eppocode"])
    taxonomy_ranked_ = taxonomy_ranked_.rename(columns={'status':'rank'})
    taxonomy_ranked_.insert(0, "rank", taxonomy_ranked_.pop("rank"))
    taxonomy_ranked_["rank"] = np.where(taxonomy_ranked_["rank"].notnull(), "kingdom", pd.NA)
    return taxonomy_ranked_
