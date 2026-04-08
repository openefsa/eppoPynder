"""This module contains core functions for working with the Country endpoint of
the EPPO API.
"""

from enum import StrEnum

from eppopynder._utils import _checks, _requests, _data


class CountryService(StrEnum):
    """The list of services supported by the Country endpoint."""
    OVERVIEW = "overview"
    CATEGORIZATION = "categorization"
    PRESENCE = "presence"


def _country(api_key, iso_codes, services=None):
    """Query the EPPO API Country endpoint.

    This internal function queries the Country endpoints of the EPPO Global
    Database via REST API for one or more ISO code(s) and one or more
    service(s). For each ISO code in `iso_codes`, the function sequentially
    queries all specified `services` and returns the extracted data through a
    list of dataframes.

    Args:
        api_key (str): The API key used for authentication.
        iso_codes (list[str]): One or more ISO codes to query.
        services (list[CountryService], optional): One or more Country services
            to query. A validation step ensures that all provided services are
            of type `CountryService` and match the supported service names. If
            not provided, all services are considered.

    Returns:
        dict: A dictionary, in which each entry corresponds to the data
            retrieved for each specified service. Each element contains a data
            frame with the queried content for all the specified ISO codes.
    """

    _checks._require_type(value=api_key, expected_type=str)
    _checks._require_type(value=iso_codes, expected_type=list)
    _checks._require_list_of(items=iso_codes, expected_type=str)
    if services is None:
        services = list(CountryService)
    _checks._require_type(value=services, expected_type=list)
    _checks._check_services(
        services=services,
        choices=list(CountryService)
    )

    country_data_ = {
        service_: {
            iso_code_: _requests._fetch_service(
                base_path='/country',
                api_key=api_key,
                code=iso_code_,
                service=service_
            )
            for iso_code_ in iso_codes
        }
        for service_ in services
    }

    country_data_ = _data._merge_batch(
        datasets=country_data_,
        parent_column_name="queried_iso_code"
    )

    return country_data_
