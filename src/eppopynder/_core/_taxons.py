"""This module contains core functions for working with the Taxons endpoint of
the EPPO API.
"""

from enum import StrEnum

from eppopynder._utils import _checks, _requests, _data


class TaxonsService(StrEnum):
    """The list of services supported by the Taxons endpoint."""
    LIST = "list"


def _taxons(api_key, services=None, params=None):
    """Query the EPPO API Taxons endpoint.

    This internal function queries the Taxons endpoints of the EPPO Global
    Database via REST API. The function sequentially queries all specified
    `services` and returns the extracted data.

    Args:
        api_key (str): The API key used for authentication.
        services (list[TaxonsService], optional): One or more Taxons services
            to query. A validation step ensures that all provided services are
            of type `TaxonsService` and match the supported service names. If
            not provided, all services are considered.
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
        services = list(TaxonsService)
    _checks._require_type(value=services, expected_type=list)
    _checks._check_services(services=services, choices=list(TaxonsService))
    if params is not None:
        _checks._require_type(value=params, expected_type=dict)

    taxons_data_ = {
        service_: _requests._fetch_service(
            base_path="/taxons",
            api_key=api_key,
            service=service_,
            params=params.get(service_, None)
            if params is not None else None
        )
        for service_ in services
    }

    taxons_data_ = _data._transform_taxons(taxons_data=taxons_data_)

    return taxons_data_
