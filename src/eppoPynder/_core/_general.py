"""This module contains core functions for working with the General endpoint of
the EPPO API.
"""

from enum import StrEnum

from eppopynder._utils import _checks, _requests


class GeneralService(StrEnum):
    """The list of services supported by the General endpoint."""
    STATUS = "status"


def _general(api_key, services=None):
    """Query the EPPO API General endpoint.

    This internal function queries the General endpoints of the EPPO Global
    Database via REST API. The function sequentially queries all specified
    `services` and returns the extracted data.

    Args:
        api_key (str): The API key used for authentication.
        services (list[GeneralService], optional): One or more General services
            to query. A validation step ensures that all provided services are
            of type `GeneralService` and match the supported service names. If
            not provided, all services are considered.

    Returns:
        dict: A dictionary, in which each entry corresponds to the data
            retrieved for each specified service. Each element contains a data
            frame with the queried content.
    """

    _checks._require_type(value=api_key, expected_type=str)
    if services is None:
        services = list(GeneralService)
    _checks._require_type(value=services, expected_type=list)
    _checks._check_services(
        services=services,
        choices=list(GeneralService)
    )

    general_data_ = {
        service_: _requests._fetch_service(
            base_path='/',
            api_key=api_key,
            service=service_
        )
        for service_ in services
    }

    return general_data_
