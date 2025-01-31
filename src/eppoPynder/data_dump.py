from eppoPynder.query_the_eppo_for_service import query_the_eppo_for_service
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

def data_dump(codes_to_scan, token = os.getenv('EPPO_token')):
    """
    Create a dump of the whole EPPO database via REST API for one or more EPPO code(s).
    
    Parameters
    ----------
    codes_to_scan : list of str
        One or more EPPO code(s) as a list of strings.

    token : str, optional
        Manually add your unique token or set it inside a .env file.
        Default is retrieved from the environment variable EPPO_token using os.getenv('EPPO_token').

    Returns
    -------
    dump : dict of {str : pd.DataFrame}
        A dictionary of pandas dataframes, each containing basic information, all names, taxonomy, categorization, hosts, pests and kingdom data about the input EPPO code, respectively.
        The dataframes will also include the following columns:
            - queried_eppocode: The EPPO code requested.
            - queried_on: The date when the query was performed.
            - queried_url: The URL that was queried.

    Examples
    --------
    # Create a dump of all data about Bemisia tabaci: basic information, all names, taxonomy, categorization, hosts, pests and kingdom data.
    data_dump(["BEMITA"])

    # Create a dump of all data about Aphis pomi and Leucoptera malifoliella: basic information, all names, taxonomy, categorization, hosts, pests and kingdom data.
    data_dump(["APHIPO", "LEUCSC"])
    """
    if not token:
        token = "default_token"
    else:
        assert isinstance(token, str), "token must be a string!"

    if not isinstance(codes_to_scan, list):
        raise AssertionError("Input must be a list!")
    if not codes_to_scan:
        raise AssertionError("Input list cannot be empty!")
    if not all(isinstance(code, str) for code in codes_to_scan):
        raise AssertionError("All codes must be strings!")

    general = pd.concat([query_the_eppo_for_service(queried_eppocode=i, service="", token=token) for i in codes_to_scan])
    general.insert(0, "pestCode", general[["queried_eppocode"]], True)
    
    names = pd.concat([query_the_eppo_for_service(queried_eppocode=i, service="names", token=token) for i in codes_to_scan])
    names.insert(0, "pestCode", names[["queried_eppocode"]], True)
    
    taxonomy = pd.concat([query_the_eppo_for_service(queried_eppocode=i, service="taxonomy", token=token) for i in codes_to_scan])
    taxonomy.insert(0, "pestCode", taxonomy[["queried_eppocode"]], True)
    
    categorization = pd.concat([query_the_eppo_for_service(queried_eppocode=i, service="categorization", token=token) for i in codes_to_scan])
    categorization.insert(0, "pestCode", categorization[["queried_eppocode"]], True)
    
    hosts = pd.concat([query_the_eppo_for_service(queried_eppocode=i, service="hosts", token=token) for i in codes_to_scan])
    hosts.insert(0, "pestCode", hosts[["queried_eppocode"]], True)
    
    pests = pd.concat([query_the_eppo_for_service(queried_eppocode=i, service="pests", token=token) for i in codes_to_scan])
    pests.insert(0, "pestCode", pests[["queried_eppocode"]], True)
    
    kingdom = pd.concat([query_the_eppo_for_service(queried_eppocode=i, service="kingdom", token=token) for i in codes_to_scan])
    kingdom.insert(0, "pestCode", kingdom[["queried_eppocode"]], True)
    
    dump = {"general":general, "names":names, "taxonomy":taxonomy, "categorization":categorization, "hosts":hosts, "pests":pests, "kingdom":kingdom}
    
    return dump 
