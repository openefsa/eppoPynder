"""This module contains core functions for working with the Reporting Service
endpoint of the EPPO API.
"""

from enum import StrEnum

from eppopynder._utils import _checks, _requests


class ReportingServiceService(StrEnum):
    """The list of services supported by the Reporting Service endpoint."""
    LIST = "list"
    REPORTING = "reporting"
    ARTICLE = "article"


def _reporting_service(api_key, services=None, params=None):
    """Query the EPPO API Reporting Service endpoint.

    This internal function queries the Reporting Service endpoints of the EPPO
    Global Database via REST API. The function sequentially queries all
    specified `services` and returns the extracted data through a dictionary of
    data frames.

    Args:
        api_key (str): The API key used for authentication.
        services (list[ReportingServiceService], optional): One or more
            Reporting Service services to query. A validation step ensures that
            all provided services are of type `ReportingServiceService` and
            match the supported service names. If not provided, all services
            are considered.
        params (dict, optional): A named dictionary of query parameters to
            include in the request. The list of available parameters can be
            accessed via the EPPO API Documentation platform
            (https://data2025.eppo.int/ui/#/docs/GDAPI).

    Returns:
        dict: A dictionary, in which each entry corresponds to the data
            retrieved for each specified service. Each element contains a data
            frame with the queried content.
    """

    _checks._require_type(value=api_key, expected_type=str)
    if services is None:
        services = list(ReportingServiceService)
    _checks._require_type(value=services, expected_type=list)
    _checks._check_services(services=services,
                            choices=list(ReportingServiceService))
    if params is not None:
        _checks._require_type(value=params, expected_type=dict)

    reporting_service_data_ = {
        service_: _requests._fetch_service(
            base_path="/reportings",
            api_key=api_key,
            service=_requests._build_reporting_service_path(
                service=service_,
                params=params.get(service_, None)
                if params is not None else None
            )
        )
        for service_ in services
    }

    return reporting_service_data_
