from eppoPynder.api_query import api_query
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

def query_the_eppo_for_service(queried_eppocode, base_url = "https://data.eppo.int/api/rest/1.0/taxon/", service = "categorization", token = os.getenv('EPPO_token')):
    """
    Query the EPPO database via REST API by specifying the name of the required service to retrieve 
    basic information, all names, taxonomy, categorization, hosts, pests, or kingdom data 
    about an EPPO code.

    Parameters
    ----------
    queried_eppocode : str
        A single EPPO code. EPPO codes are unique computer codes developed for plants and pests 
        (including pathogens) important in agriculture and plant protection. These codes 
        facilitate the management of plant and pest names in databases and enable data exchange 
        between IT systems. Each EPPO code consists of 5 to 6 letters, often mnemonic 
        abbreviations of the scientific name of the organism, and can be freely downloaded 
        from the EPPO Data Services platform at https://data.eppo.int/.

    base_url : str, optional
        URL root for all REST API requests. Default is "https://data.eppo.int/api/rest/1.0".

    service : str, optional
        The specific service to query. Choose from the following options:
            - "" : basic information
            - "names" : all names
            - "taxonomy" : taxonomy data
            - "categorization" : categorization data
            - "hosts" : hosts data
            - "pests" : pests data
            - "kingdom" : kingdom taxonomic rank
        Default is "categorization".

    token : str, optional
        Manually add your unique token or set it inside a .env file.
        Default is retrieved from the environment variable EPPO_token using os.getenv('EPPO_token').

    Returns
    -------
    queried_service : pd.DataFrame
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
    query_the_eppo_for_service("BEMITA", service="")

    # Get all names for Bemisia tabaci:
    query_the_eppo_for_service("BEMITA", service="names")

    # Get categorization data for Bemisia tabaci:
    query_the_eppo_for_service("BEMITA", service="categorization")
    """
    # Ensure the token is available
    if not token:
        raise ValueError("EPPO token is required. Please provide a valid token.")

    assert isinstance(queried_eppocode, str), "queried_eppocode must be a string!"
    assert isinstance(base_url, str), "base_url must be a string!"
    assert isinstance(service, str), "service must be a string!"
    assert isinstance(token, str), "token must be a string!"
    
    queried_url = base_url+queried_eppocode+"/"+service+"?authtoken="+token
    
    if service == "":
        queried_url = base_url+queried_eppocode+"?authtoken="+token
    
    queried_service = api_query(queried_eppocode=queried_eppocode, queried_url=queried_url)
    
    return queried_service
    
