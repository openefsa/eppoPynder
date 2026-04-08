import os
from dotenv import load_dotenv

from eppopynder._utils import _checks
from eppopynder._core import (_general, _taxons, _taxon, _country, _rppo,
                              _tools, _reporting_service, _references)


class Client:
    """Client class for working with the EPPO API.

    Attributes:
        _api_key (str): The API key used for authentication.

    Methods:
        general(services): Query the EPPO API General endpoint.
        taxons(services, params): Query the EPPO API Taxons endpoint.
        taxon(eppo_codes, services): Query the EPPO API Taxon endpoint.
        country(iso_codes, services): Query the EPPO API Country endpoint.
        rppo(rppo_codes, services): Query the EPPO API RPPO endpoint.
        tools(services, params): Query the EPPO API Tools endpoint.
        reporting_service(services, params): Query the EPPO API Reporting
            Service endpoint.
        references(services): Query the EPPO API References endpoint.
    """

    def __init__(self, api_key=None):
        """Initialize the client.

        Args:
            api_key (str, optional): The API key used for authentication.

        Examples:
            >>> from eppopynder import Client

            >>> # Create a client using the API key defined in the .env file.
            >>> client_with_default = Client()

            >>> # Create a client using a manually specified API key.
            >>> client_with_api_key = Client(api_key="<your_api_key>")
        """

        if api_key is not None:
            self._api_key = api_key
        else:
            load_dotenv()
            self._api_key = os.getenv("EPPO_API_KEY")

            if self._api_key is None:
                raise ValueError(
                    "The EPPO_API_KEY environment variable is not set")

        _checks._require_type(value=self._api_key, expected_type=str)

        if not self._api_key.strip():
            raise ValueError("The API key can not be empty")

    def general(self, services=None):
        """Query the EPPO API General endpoint.

        This function queries the General endpoints of the EPPO Global Database
        via REST API. The function sequentially queries all specified
        `services` and returns the extracted data.

        Args:
            services (list[GeneralService], optional): One or more General
                services to query. A validation step ensures that all provided
                services are of type `GeneralService` and match the supported
                service names. If not provided, all services are considered.

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content.
                
        Examples:
            >>> from eppopynder import Client, GeneralService
            
            >>> client = Client()
            
            >>> # Get information about system health status.
            >>> data = client.general(services=[GeneralService.STATUS])
        """
        
        return _general._general(api_key=self._api_key, services=services)

    def taxons(self, services=None, params=None):
        """Query the EPPO API Taxons endpoint.

        This function queries the Taxons endpoints of the EPPO Global Database
        via REST API. The function sequentially queries all specified
        `services` and returns the extracted data.

        Args:
            services (list[TaxonsService], optional): One or more Taxons
                services to query. A validation step ensures that all provided
                services are of type `TaxonsService` and match the supported
                service names. If not provided, all services are considered.
            params (dict, optional): A named dictionary of query parameters to
                include in the request. The list of available parameters can be
                accessed via the EPPO API Documentation platform
                (https://data2025.eppo.int/ui/#/docs/GDAPI).

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content.

        Examples:
            >>> from eppopynder import Client, TaxonsService

            >>> client = Client()

            >>> # Get the list of taxons with default parameters.
            >>> data = client.taxons(services=[TaxonsService.LIST])

            >>> # Get the list of taxons with custom parameters.
            ... data = client.taxons(
            ...     services=[TaxonsService.LIST],
            ...     params={
            ...         "list": {
            ...             "createdFromDate": "2000-01-01",
            ...             "limit": 5,
            ...             "offset": 100,
            ...             "orderAsc": False,
            ...             "orderBy": "eppocode"
            ...         }
            ...     }
            ... )
        """

        return _taxons._taxons(api_key=self._api_key, services=services,
                               params=params)

    def taxon(self, eppo_codes, services=None):
        """Query the EPPO API Taxon endpoint.

        This function queries the Taxon endpoints of the EPPO Global Database
        via REST API for one or more EPPO code(s) and one or more service(s).
        For each EPPO code in `eppo_codes`, the function sequentially queries
        all specified `services` and returns the extracted data.

        Args:
            eppo_codes (list[str]): One or more EPPO codes to query.
            services (list[TaxonService], optional): One or more Taxon services
                to query. A validation step ensures that all provided services
                are of type `TaxonService` and match the supported service
                names. If not provided, all services are considered.

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content for all the specified EPPO
                codes.

        Examples:
            >>> from eppopynder import Client, TaxonService

            >>> client = Client()

            >>> # Get all information about Bemisia tabaci.
            >>> data = client.taxon(eppo_codes=["BEMITA"])

            >>> # Get names data about Bemisia tabaci.
            >>> data = client.taxon(
            ...     eppo_codes=["BEMITA"],
            ...     services=[TaxonService.NAMES]
            ... )

            >>> # Get taxonomy and categorization data about Bemisia tabaci and
            >>> # Gossypium hirsutum.
            >>> data = client.taxon(
            ...     eppo_codes=["BEMITA", "GOSHI"],
            ...     services=[
            ...         TaxonService.TAXONOMY,
            ...         TaxonService.CATEGORIZATION
            ...     ]
            ... )
        """

        return _taxon._taxon(api_key=self._api_key, eppo_codes=eppo_codes,
                             services=services)

    def country(self, iso_codes, services=None):
        """Query the EPPO API Country endpoint.

        This function queries the Country endpoints of the EPPO Global Database
        via REST API for one or more ISO code(s) and one or more service(s).
        For each ISO code in `iso_codes`, the function sequentially queries all
        specified `services` and returns the extracted data through a list of
        dataframes.

        Args:
            iso_codes (list[str]): One or more ISO codes to query.
            services (list[CountryService], optional): One or more Country
                services to query. A validation step ensures that all provided
                services are of type `CountryService` and match the supported
                service names. If not provided, all services are considered.

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content for all the specified ISO
                codes.
                
        Examples:
            >>> from eppopynder import Client, CountryService
            
            >>> client = Client()
            
            >>> # Get all information about France.
            >>> data = client.country(iso_codes=["FR"])
            
            >>> # Get overview data about France.
            >>> data = client.country(
            ...     iso_codes=["FR"],
            ...     services=[CountryService.OVERVIEW]
            ... )
            
            >>> # Get overview and categorization data about France and Italy.
            >>> data = client.country(
            ...     iso_codes=["FR", "IT"],
            ...     services=[
            ...         CountryService.OVERVIEW,
            ...         CountryService.CATEGORIZATION
            ...     ]
            ... )
        """
        
        return _country._country(api_key=self._api_key, iso_codes=iso_codes,
                                 services=services)

    def rppo(self, rppo_codes, services=None):
        """Query the EPPO API RPPO endpoint.

        This function queries the RPPO endpoints of the EPPO Global Database
        via REST API for one or more RPPO code(s) and one or more service(s).
        For each RPPO code in `rppo_codes`, the function sequentially queries
        all specified `services` and returns the extracted data through a list
        of dataframes.

        Args:
            rppo_codes (list[str]): One or more RPPO codes to query.
            services (list[CountryService], optional): One or more RPPO
                services to query. A validation step ensures that all provided
                services are of type `RPPOService` and match the supported
                service names. If not provided, all services are considered.

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content for all the specified RPPO
                codes.

        Examples:
            >>> from eppopynder import Client, RPPOService

            >>> client = Client()

            >>> # Get all information about the European and Mediterranean
            >>> # Plant Protection Organisation.
            >>> data = client.rppo(rppo_codes=["9A"])

            >>> # Get overview data about the European and Mediterranean
            >>> # Plant Protection Organisation.
            >>> data = client.rppo(
            ...     rppo_codes=["9A"],
            ...     services=[RPPOService.OVERVIEW]
            ... )

            >>> # Get overview and categorization data about the European and
            >>> # Mediterranean Plant Protection Organisation and the European
            >>> # Union.
            >>> data = client.rppo(
            ...     rppo_codes=["9A", "9L"],
            ...     services=[
            ...         RPPOService.OVERVIEW,
            ...         RPPOService.CATEGORIZATION
            ...     ]
            ... )
        """

        return _rppo._rppo(api_key=self._api_key, rppo_codes=rppo_codes,
                                 services=services)

    def tools(self, services=None, params=None):
        """Query the EPPO API Tools endpoint.

        This function queries the Tools endpoints of the EPPO Global Database
        via REST API. The function sequentially queries all specified
        `services` and returns the extracted data through a dictionary of data
        frames.

        Args:
            services (list[ToolsService], optional): One or more Tools services
                to query. A validation step ensures that all provided services
                are of type `ToolsService` and match the supported service
                names. If not provided, all services are considered.
            params (dict, optional): A named dictionary of query parameters to
                include in the request. The list of available parameters can be
                accessed via the EPPO API Documentation platform
                (https://data2025.eppo.int/ui/#/docs/GDAPI).

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content.
                
        Examples:
            >>> from eppopynder import Client, ToolsService
            
            >>> client = Client()
            
            >>> # Get the EPPO codes associated to the name Bemisia tabaci.
            >>> data = client.tools(
            ...     services=[ToolsService.NAME2CODES],
            ...     params={
            ...         ToolsService.NAME2CODES: {
            ...             "name": "Bemisia tabaci",
            ...             "onlyPreferred": False
            ...         }
            ...     }
            ... )
        """
        
        return _tools._tools(api_key=self._api_key, services=services,
                             params=params)

    def reporting_service(self, services=None, params=None):
        """Query the EPPO API Reporting Service endpoint.

        This function queries the Reporting Service endpoints of the EPPO
        Global Database via REST API. The function sequentially queries all
        specified `services` and returns the extracted data through a
        dictionary of data frames.

        Args:
            services (list[ReportingServiceService], optional): One or more
                Reporting Service services to query. A validation step ensures
                that all provided services are of type
                `ReportingServiceService` and match the supported service
                names. If not provided, all services are considered.
            params (dict, optional): A named dictionary of query parameters to
                include in the request. The list of available parameters can be
                accessed via the EPPO API Documentation platform
                (https://data2025.eppo.int/ui/#/docs/GDAPI).

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content.
                
        Examples:
            >>> from eppopynder import Client, ReportingServiceService
            
            >>> client = Client()
            
            >>> # Get the list of reporting service issues.
            >>> data = client.reporting_service(
            ...     services=[ReportingServiceService.LIST]
            ... )
            
            >>> # Get a specific reporting service issue.
            >>> data = client.reporting_service(
            ...     services=[ReportingServiceService.REPORTING],
            ...     params={
            ...         ReportingServiceService.REPORTING: {
            ...             "reporting_id": 10
            ...         }
            ...     }
            ... )
            
            >>> # Get a specific article.
            >>> data = client.reporting_service(
            ...     services=[ReportingServiceService.ARTICLE],
            ...     params={
            ...         ReportingServiceService.ARTICLE: {
            ...             "article_id": 234
            ...         }
            ...     }
            ... )
            
            >>> # Get the list of reporting service issues, a specific
            >>> # reporting service issue and a specific article.
            >>> data = client.reporting_service(
            ...     params={
            ...         ReportingServiceService.REPORTING: {
            ...             "reporting_id": 10
            ...         },
            ...         ReportingServiceService.ARTICLE: {
            ...             "article_id": 234
            ...         }
            ...     }
            ... )
        """
        
        return _reporting_service._reporting_service(
            api_key=self._api_key,
            services=services,
            params=params
        )

    def references(self, services=None):
        """Query the EPPO API References endpoint.

        This function queries the References endpoints of the EPPO Global
        Database via REST API. The function sequentially queries all specified
        `services` and returns the extracted data through a dictionary of data
        frames.

        Args:
            services (list[ReferencesService], optional): One or more
                References services to query. A validation step ensures that
                all provided services are of type `ReferencesService` and match
                the supported service names. If not provided, all services are
                considered.

        Returns:
            dict: A dictionary, in which each entry corresponds to the data
                retrieved for each specified service. Each element contains a
                data frame with the queried content.

        Examples:
            >>> from eppopynder import Client, ReferencesService

            >>> client = Client()

            >>> # Get all references information.
            >>> data = client.references()

            >>> # Get information about distribution status codes.
            >>> data = client.references(
            ...     services=[ReferencesService.DISTRIBUTION_STATUS]
            ... )

            # Get information about EPPO list codes and labels and countries.
            >>> data = client.references(
            ...     services=[
            ...         ReferencesService.Q_LIST,
            ...         ReferencesService.COUNTRIES
            ...     ]
            ... )
        """

        return _references._references(
            api_key=self._api_key,
            services=services
        )
