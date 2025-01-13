def unnest_lists(json_response): 
    """
    Unnest nested lists and dictionaries in a JSON dictionary of host data retrieved from EPPO.
    
    Parameters
    ----------
    json_response : dict
        A JSON dictionary of nested lists and dictionaries containing the contents of a request.
        
    Returns
    -------
    json_response : list
        A list of JSON dictionaries containing the contents of a request.
    """
    if type(json_response) is dict and len(json_response)>0 and ("Major host" in json_response or "Host" in json_response or "Wild/Weed" in json_response or "Alternate" in json_response or "Experimental" in json_response or "Doubtful host" in json_response or "Non-host" in json_response):
      unnest_hosts = (json_response.get("Major host") if json_response.get("Major host") is not None else []) + \
      (json_response.get("Host") if json_response.get("Host") is not None else []) + \
      (json_response.get("Wild/Weed") if json_response.get("Wild/Weed") is not None else []) + \
      (json_response.get("Alternate") if json_response.get("Alternate") is not None else []) + \
      (json_response.get("Experimental") if json_response.get("Experimental") is not None else []) + \
      (json_response.get("Doubtful host") if json_response.get("Doubtful host") is not None else []) + \
      (json_response.get("Non-host") if json_response.get("Non-host") is not None else [])
      json_response = unnest_hosts

    return json_response
