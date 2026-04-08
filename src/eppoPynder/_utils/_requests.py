"""This module contains internal functions for working with EPPO API requests.
"""

import pandas as pd
import requests
from datetime import datetime
from json import JSONDecodeError

from eppopynder._utils import _checks
from eppopynder._utils import _data


def _build_endpoint(base_path, code=None, service=None):
    """Build an EPPO API endpoint path.

    This helper function constructs an endpoint path for retrieving data from
    the EPPO API. The result must be appended to the EPPO API base URL. It
    allows for the optional inclusion of a specific code and/or service name,
    depending on the desired API resource. The function is based on the fact
    that EPPO API endpoints follow the pattern:
    {base path}/{resource identifier}/{service}.

    Args:
        base_path (str): The base path, starting with '/' (e.g.
            "/taxons/taxon").
        code (str, optional): The resource identifier (e.g. an EPPO code or
            an ISO code). If provided, it will be appended to the base path.
        service (str, optional): The desired API service. If provided, it will
            be appended to the path after the resource identifier (if any,
            otherwise after the base path).

    Returns:
        str: A string representing the complete endpoint path to be used in an
            API request.
    """

    _checks._require_type(value=base_path, expected_type=str)
    _checks._require_trailing_slash(string=base_path)
    if code is not None:
        _checks._require_type(value=code, expected_type=str)
    if service is not None:
        _checks._require_type(value=service, expected_type=str)

    endpoint_parts_ = [base_path] + [part_ for part_ in (code, service)
                                     if part_ is not None]
    endpoint_path_ = '/'.join(endpoint_parts_)
    endpoint_path_ = endpoint_path_.replace("//", '/')

    return endpoint_path_


def _build_reporting_service_path(service, params = None):
    """Build the EPPO reporting-related service path.

    This helper function constructs the endpoint path for EPPO API reporting
    services based on the service type and parameters provided in the `params`
    dictionary. It also handles missing or invalid parameters by raising
    informative errors.

    Args:
        service (str): The type of service. Supported values are `reporting`
            and `article`.
        params (dict, optional): A dictionary containing identifiers needed for
            the endpoint path. Must include `reporting_id` if service is
            "reporting" or `article_id` if service is "article".

    Raises:
        ValueError: If a required parameter is missing or invalid for the
            specified service.

    Returns:
        str: The constructed service path to use with API calls.
    """

    _checks._require_type(value=service, expected_type=str)
    if params is not None:
        _checks._require_type(value=params, expected_type=dict)

    required_ids_ = {
        "reporting": "reporting_id",
        "article": "article_id",
    }

    required_id_name_ = required_ids_.get(service)

    if required_id_name_ is not None:
        if params is None or not params.get(required_id_name_):
            raise ValueError("Missing required parameter " +
                             f"\"{required_id_name_}\"")

        service = f"{service}/{params[required_id_name_]}"

    return service


def _perform_request(url, api_key, params=None):
    """Build and execute an HTTP GET request to the EPPO API.

    This helper function prepares and sends a GET request to the EPPO API,
    setting the necessary headers, authentication key and query parameters. It
    then performs the request and returns the corresponding response data.

    Args:
        url (str): The full API endpoint URL to query.
        api_key (str): The API key used for authentication.
        params (dict, optional): Optional query parameters to include in the
            request.

    Returns:
        class (requests.Response): The HTTP response object returned by
            the request.
    """

    _checks._require_type(value=url, expected_type=str)
    _checks._require_type(value=api_key, expected_type=str)
    if params is not None:
        _checks._require_type(value=params, expected_type=dict)

    request_headers_ = {
        "X-Api-Key": api_key,
        "Accept": "application/json"
    }

    response_ = requests.get(url, headers=request_headers_, params=params)

    return response_


def _handle_http_errors(response):
    """Handle non-successful HTTP responses from the EPPO API.

    This helper function checks whether an HTTP response from the EPPO API
    indicates success (status code 200). If the response contains any other
    status code, it attempts to parse the JSON body for an error message and
    raises a formatted error.

    Args:
        response (requests.Response): The HTTP response object.

    Raises:
        requests.exceptions.HTTPError: If the request was not successful.

    Returns:
        None: The function returns nothing if the request was successful.
    """

    _checks._require_type(value=response, expected_type=requests.Response)

    handled_error_status_codes_ = [400, 401, 403, 404, 429, 500]

    if response.status_code == 200:
        return

    if response.status_code in handled_error_status_codes_:
        try:
            error_message_ = response.json().get("error", "Unknown error")
        except JSONDecodeError as e_:
            error_message_ = e_.msg
        raise requests.HTTPError(f"API request failed: {error_message_}")

    raise requests.HTTPError("API request failed with status code "
                             + f"{response.status_code}")


def _parse_response(response):
    """Parse a JSON API response.

    This helper function parses the JSON body of an API response.

    Args:
        response (requests.Response): The HTTP response object.

    Raises:
        JSONDecodeError: If the response body can not be parsed as valid JSON.

    Returns:
        DataFrame: A Pandas DataFrame representing the parsed JSON response.
    """

    _checks._require_type(value=response, expected_type=requests.Response)

    try:
        response_json_ = response.json()
        response_data_ = _data._flatten(response_json_)
    except (JSONDecodeError, KeyError) as e_:
        raise JSONDecodeError(f"Failed to parse API response: {e_.msg}",
                              e_.doc, e_.pos)

    return response_data_


def _enrich_response(response_data, url):
    """Enrich API response data.

    This helper function takes a structure containing API response data and
    enriches it with metadata, including the timestamp and the queried URL.

    Args:
        response_data (DataFrame): A structure containing the API response
            data.
        url (str): The URL that was queried.

    Returns:
        DataFrame: A Pandas DataFrame containing the original API response
        data, along with two additional fields: `queried_on`, the timestamp
        when the data was queried, and `queried_url`, the URL used for
        the API request.
    """

    _checks._require_type(value=response_data, expected_type=pd.DataFrame)
    _checks._require_type(value=url, expected_type=str)

    response_data["queried_on"] = datetime.now()
    response_data["queried_url"] = url

    return response_data


def _query(endpoint, api_key, params=None):
    """Query the EPPO REST API and return the result.

    This function performs a GET request to the EPPO REST API, automatically
    builds the full request URL, adds the authentication header, handles HTTP
    errors, parses the response and adds metadata about the query.

    Specific HTTP status codes (400, 401, 403, 404, 429 and 500) are handled
    explicitly to extract the error message returned by the API; other status
    codes trigger a connection error.

    Args:
        endpoint (str): The relative path of the endpoint to query, starting
            with a forward slash (`/`).
        api_key (str): The API key used for authentication.
        params (dict, optional): Optional query parameters to include in the
            request.

    Returns:
        DataFrame: A Pandas DataFrame containing the parsed JSON response from
        the API, along with metadata fields.
    """

    _checks._require_type(value=endpoint, expected_type=str)
    _checks._require_trailing_slash(string=endpoint)
    _checks._require_type(value=api_key, expected_type=str)
    if params is not None:
        _checks._require_type(value=params, expected_type=dict)

    base_url_ = "https://api.eppo.int/gd/v2"
    full_url_ = base_url_ + endpoint

    response_ = _perform_request(
        url=full_url_,
        api_key=api_key,
        params=params
    )

    _handle_http_errors(response=response_)

    response_data_ = _parse_response(response=response_)

    enriched_data_ = _enrich_response(response_data=response_data_,
                                      url=full_url_)

    return enriched_data_


def _fetch_service(base_path, api_key, code=None, service=None,
                   params=None):
    """Fetch data from a specific EPPO API service.

    This function retrieves data from a specific service of the EPPO API. It
    builds the appropriate endpoint according to the EPPO API structure, then
    queries the API.

    Args:
        base_path (str): The base path, starting with '/' (e.g.
            "/taxons/taxon").
        api_key (str): The API key used for authentication.
        code (str, optional): The resource identifier (e.g. an EPPO code or an
            ISO code).
        service (str, optional): The desired API service.
        params (dict, optional): Optional query parameters to include in the
            request.

    Returns:
        DataFrame: A Pandas DataFrame containing the data returned by the
            specified EPPO API service, along with metadata fields.
    """

    _checks._require_type(value=base_path, expected_type=str)
    _checks._require_trailing_slash(string=base_path)
    _checks._require_type(value=api_key, expected_type=str)
    if code is not None:
        _checks._require_type(value=code, expected_type=str)
    if service is not None:
        _checks._require_type(value=service, expected_type=str)
    if params is not None:
        _checks._require_type(value=params, expected_type=dict)

    service_endpoint_ = _build_endpoint(
        base_path=base_path,
        code=code,
        service=service
    )

    service_data_ = _query(endpoint=service_endpoint_, api_key=api_key,
                           params=params)

    return service_data_
