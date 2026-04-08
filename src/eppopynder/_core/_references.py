"""This module contains core functions for working with the References endpoint
of the EPPO API.
"""

from enum import StrEnum

from eppopynder._utils import _checks, _requests, _data


class ReferencesService(StrEnum):
    """The list of services supported by the References endpoint."""
    RPPOS = "rppos"
    Q_LIST = "qList"
    DISTRIBUTION_STATUS = "distributionStatus"
    PEST_HOST_CLASSIFICATION = "pestHostClassification"
    VECTOR_CLASSIFICATION = "vectorClassification"
    COUNTRIES = "countries"
    COUNTRIES_STATES = "countriesStates"


def _references(api_key, services=None):
    """Query the EPPO API References endpoint.

    This internal function queries the References endpoints of the EPPO Global
    Database via REST API. The function sequentially queries all specified
    `services` and returns the extracted data through a dictionary of data
    frames.

    Args:
        api_key (str): The API key used for authentication.
        services (list[ReferencesService], optional): One or more References
            services to query. A validation step ensures that all provided
            services are of type `ReferencesService` and match the supported
            service names. If not provided, all services are considered.

    Returns:
        dict: A dictionary, in which each entry corresponds to the data
            retrieved for each specified service. Each element contains a data
            frame with the queried content.
    """

    _checks._require_type(value=api_key, expected_type=str)
    if services is None:
        services = list(ReferencesService)
    _checks._require_type(value=services, expected_type=list)
    _checks._check_services(
        services=services,
        choices=list(ReferencesService)
    )

    references_data_ = {
        service_: _requests._fetch_service(
            base_path='/references',
            api_key=api_key,
            service=service_
        )
        for service_ in services
    }

    references_data_ = _data._transform_references(
        references_data=references_data_)

    return references_data_
