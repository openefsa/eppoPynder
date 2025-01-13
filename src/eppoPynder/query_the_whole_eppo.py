from eppoPynder.query_the_eppo_for_service import query_the_eppo_for_service
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

def query_the_whole_eppo(queried_eppocode, base_url = "https://data.eppo.int/api/rest/1.0/taxon/", token = os.getenv('EPPO_token')):
    """
    Query the EPPO database via REST API to retrieve basic information, 
    all names, taxonomy, categorization, hosts, pests, and kingdom data about an EPPO code.

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

    token : str, optional
        Manually add your unique token or set it inside a .env file.
        Default is retrieved from the environment variable EPPO_token using os.getenv('EPPO_token').

    Returns
    -------
    EPPO_dict : dict of {str : pd.DataFrame}
        A dictionary of pandas dataframes, each containing basic information, all names, taxonomy, categorization, hosts, pests and kingdom data about the input EPPO code, respectively.
        The dataframes will also include the following columns:
            - queried_eppocode: The EPPO code requested.
            - queried_on: The date when the query was performed.
            - queried_url: The URL that was queried.

    Examples
    --------
    # Get all information about Bemisia tabaci: basic information, all names, taxonomy, 
    # categorization, hosts, pests, and kingdom data.
    query_the_whole_eppo("BEMITA")
    """
    # Ensure the token is available
    if not token:
        raise ValueError("EPPO token is required. Please provide a valid token.")
        
    assert isinstance(queried_eppocode, str), "queried_eppocode must be a string!"
    assert isinstance(base_url, str), "base_url must be a string!"
    assert isinstance(token, str), "token must be a string!"
    
    services = ["", "names", "taxonomy", "categorization", "hosts", "pests", "kingdom"]
    
    EPPO_list = []
    
    for service in services:
        EPPO_list.append(query_the_eppo_for_service(queried_eppocode=queried_eppocode, base_url=base_url, service=service, token=token))
    
    services[0]="general"
    EPPO_dict = {name: df for name, df in zip(services, EPPO_list)}
    
    return EPPO_dict
