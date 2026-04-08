"""This module contains core functions for working with the RPPO endpoint of
the EPPO API.
"""

from enum import StrEnum

from eppopynder._utils import _checks, _requests, _data


class RPPOService(StrEnum):
    """The list of services supported by the RPPO endpoint."""
    OVERVIEW = "overview"
    CATEGORIZATION = "categorization"


def _rppo(api_key, rppo_codes, services=None):
    """Query the EPPO API RPPO endpoint.

    This internal function queries the RPPO endpoints of the EPPO Global
    Database via REST API for one or more RPPO code(s) and one or more
    service(s). For each RPPO code in `rppo_codes`, the function sequentially
    queries all specified `services` and returns the extracted data through a
    list of dataframes.

    Args:
        api_key (str): The API key used for authentication.
        rppo_codes (list[str]): One or more RPPO codes to query.
        services (list[CountryService], optional): One or more RPPO services
            to query. A validation step ensures that all provided services are
            of type `RPPOService` and match the supported service names. If
            not provided, all services are considered.

    Returns:
        dict: A dictionary, in which each entry corresponds to the data
            retrieved for each specified service. Each element contains a data
            frame with the queried content for all the specified RPPO codes.
    """

    _checks._require_type(value=api_key, expected_type=str)
    _checks._require_type(value=rppo_codes, expected_type=list)
    _checks._require_list_of(items=rppo_codes, expected_type=str)
    if services is None:
        services = list(RPPOService)
    _checks._require_type(value=services, expected_type=list)
    _checks._check_services(
        services=services,
        choices=list(RPPOService)
    )

    rppo_data_ = {
        service_: {
            rppo_code_: _requests._fetch_service(
                base_path='/rppo',
                api_key=api_key,
                code=rppo_code_,
                service=service_
            )
            for rppo_code_ in rppo_codes
        }
        for service_ in services
    }

    rppo_data_ = _data._merge_batch(
        datasets=rppo_data_,
        parent_column_name="queried_rppo_code"
    )

    return rppo_data_
