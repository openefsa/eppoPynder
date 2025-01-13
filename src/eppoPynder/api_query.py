import numpy as np
import pandas as pd
import requests
from datetime import date

from eppoPynder.unnest_lists import unnest_lists

def api_query(queried_eppocode, queried_url):
    """
    Query the EPPO database via REST API to retrieve basic information, 
    all names, taxonomy, categorization, hosts, pests, or kingdom data about an EPPO code.

    Parameters
    ----------
    queried_eppocode : str
        A single EPPO code. EPPO codes are unique computer codes developed for plants and pests 
        (including pathogens) important in agriculture and plant protection. These codes 
        facilitate the management of plant and pest names in databases and enable data exchange 
        between IT systems. Each EPPO code consists of 5 to 6 letters, often mnemonic 
        abbreviations of the scientific name of the organism, and can be freely downloaded 
        from the EPPO Data Services platform at https://data.eppo.int/.

    queried_url : str 
        The URL to query. The URL should be in the format:
        https://data.eppo.int/api/rest/1.0/taxon/queriedEppocode?authtoken=xxxxxxxxxxxxxxxxxxx
        Replace "queriedEppocode" with the EPPO code of interest and add your unique token using the "authtoken" parameter. 

    Returns
    -------
    df : pd.DataFrame
        A dataframe containing the contents of the request converted from JSON. 
        Based on the query, the output dataframe will contain basic information, all names, 
        taxonomy, categorization, hosts, pests, or kingdom data about the input EPPO code.
        The dataframe will also include the following columns:
            - queried_eppocode: The EPPO code requested.
            - queried_on: The date when the query was performed.
            - queried_url: The URL that was queried.

    Examples
    --------
    # Get basic information about Bemisia tabaci:
    queried_eppocode = "BEMITA"
    queried_url = "https://data.eppo.int/api/rest/1.0/taxon/BEMITA?authtoken=xxxxxxxxxxxxxxxxxxx"
    api_query(queried_eppocode, queried_url)
    
    # Get taxonomy data about Bemisia tabaci:
    queried_eppocode = "BEMITA"
    queried_url = "https://data.eppo.int/api/rest/1.0/taxon/BEMITA/taxonomy?authtoken=xxxxxxxxxxxxxxxxxxx"
    api_query(queried_eppocode, queried_url)
    
    # Get all names about Aphis pomi:
    queried_eppocode = "APHIPO"
    queried_url = "https://data.eppo.int/api/rest/1.0/taxon/APHIPO/names?authtoken=xxxxxxxxxxxxxxxxxxx"
    api_query(queried_eppocode, queried_url)
    """
    assert isinstance(queried_eppocode, str), "queried_eppocode must be a string!"
    assert isinstance(queried_url, str), "queried_url must be a string!"
    
    df = pd.DataFrame()
    
    try:
        requested_service = requests.get(queried_url)
        requested_service.raise_for_status()
        json_response = requested_service.json()
        data = unnest_lists(json_response)
        df = pd.json_normalize(data)

    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL) as e:
        print(f"{e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")

    finally:
        df['queried_eppocode'] = pd.Series([queried_eppocode for i in range(len(df)+1)])
        df['queried_on'] = pd.Series([str(date.today()) for i in range(len(df)+1)])
        df['queried_url'] = pd.Series([queried_url for i in range(len(df)+1)])
        
    return df
