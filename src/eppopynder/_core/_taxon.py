"""This module contains core functions for working with the Taxon endpoint of
the EPPO API.
"""

from enum import StrEnum

from eppopynder._utils import _checks, _requests, _data


class TaxonService(StrEnum):
    """The list of services supported by the Taxon endpoint."""
    OVERVIEW = "overview"
    INFOS = "infos"
    NAMES = "names"
    TAXONOMY = "taxonomy"
    CATEGORIZATION = "categorization"
    KINGDOM = "kingdom"
    HOSTS = "hosts"
    PESTS = "pests"
    VECTORS = "vectors"
    VECTOR_OF = "vectorof"
    BCA = "bca"
    BCA_OF = "bcaof"
    PHOTOS = "photos"
    REPORTING_ARTICLES = "reporting_articles"
    DOCUMENTS = "documents"
    STANDARDS = "standards"
    DISTRIBUTION = "distribution"


def _taxon(api_key, eppo_codes, services=None):
    """Query the EPPO API Taxon endpoint.

    This internal function queries the Taxon endpoints of the EPPO Global
    Database via REST API for one or more EPPO code(s) and one or more
    service(s). For each EPPO code in `eppo_codes`, the function sequentially
    queries all specified `services` and returns the extracted data.

    Args:
        api_key (str): The API key used for authentication.
        eppo_codes (list[str]): One or more EPPO codes to query.
        services (list[TaxonService], optional): One or more Taxon services
            to query. A validation step ensures that all provided services are
            of type `TaxonService` and match the supported service names. If
            not provided, all services are considered.

    Returns:
        dict: A dictionary, in which each entry corresponds to the data
            retrieved for each specified service. Each element contains a data
            frame with the queried content for all the specified EPPO codes.
    """

    _checks._require_type(value=api_key, expected_type=str)
    _checks._require_type(value=eppo_codes, expected_type=list)
    _checks._require_list_of(items=eppo_codes, expected_type=str)
    if services is None:
        services = list(TaxonService)
    _checks._require_type(value=services, expected_type=list)
    _checks._check_services(
        services=services,
        choices=list(TaxonService)
    )

    taxon_data_ = {
        service_: {
            eppo_code_: _requests._fetch_service(
                base_path='/taxons/taxon',
                api_key=api_key,
                code=eppo_code_,
                service=service_
            )
            for eppo_code_ in eppo_codes
        }
        for service_ in services
    }

    taxon_data_ = _data._merge_batch(
        datasets=taxon_data_,
        parent_column_name="queried_eppo_code"
    )

    return taxon_data_
