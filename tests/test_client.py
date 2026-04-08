import os
import unittest
from unittest.mock import patch
from dotenv import load_dotenv

from eppopynder.client import Client
from eppopynder._core._general import GeneralService
from eppopynder._core._taxons import TaxonsService
from eppopynder._core._taxon import TaxonService
from eppopynder._core._country import CountryService
from eppopynder._core._rppo import RPPOService
from eppopynder._core._tools import ToolsService
from eppopynder._core._reporting_service import ReportingServiceService
from eppopynder._core._references import ReferencesService

load_dotenv()


class TestClient(unittest.TestCase):

    ##############
    # __init__() #
    ##############

    def test___init___types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, Client, api_key=123)
        self.assertRaises(ValueError, Client, api_key='')

    def test___init___invalid_key(self):
        """Test that ValueError is raised when EPPO_API_KEY is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("eppopynder.client.load_dotenv"):
                self.assertRaises(ValueError, Client)

    def test___init__1(self):
        """Test the correct creation of the object."""
        with patch.dict(os.environ, {
            "EPPO_API_KEY": "EPPO_API_KEY",
        }, clear=True):
            with patch("eppopynder.client.load_dotenv"):
                self.assertIsInstance(Client(api_key="EPPO_API_KEY"), Client)

    # This test requires the EPPO_API_KEY environment variable to be set.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test___init__1_online(self):
        """Test the correct creation of the object."""
        self.assertIsInstance(Client(), Client)

    def test___init__2(self):
        """Test the correct creation of the object."""
        self.assertIsInstance(Client(api_key="EPPO_API_KEY"), Client)

    #############
    # general() #
    #############

    @patch("eppopynder._core._general._general")
    def test_general(self, mock_general):
        """Test the General endpoint."""
        mock_general.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [GeneralService.STATUS]
        data_ = client_.general(services=services_)
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_general_online(self):
        """Test the General endpoint."""
        client_ = Client()
        services_ = [GeneralService.STATUS]
        data_ = client_.general(services=services_)
        self.assertIsInstance(data_, dict)

    ############
    # taxons() #
    ############

    @patch("eppopynder._core._taxons._taxons")
    def test_taxons(self, mock_taxons):
        """Test the Taxons endpoint."""
        mock_taxons.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [TaxonsService.LIST]
        data_ = client_.taxons(services=services_)
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_taxons_online(self):
        """Test the Taxons endpoint."""
        client_ = Client()
        services_ = [TaxonsService.LIST]
        data_ = client_.taxons(services=services_)
        self.assertIsInstance(data_, dict)

    ###########
    # taxon() #
    ###########

    @patch("eppopynder._core._taxon._taxon")
    def test_taxon(self, mock_taxon):
        """Test the Taxon endpoint."""
        mock_taxon.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [TaxonService.OVERVIEW]
        data_ = client_.taxon(eppo_codes=["BEMITA"], services=services_)
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_taxon_online(self):
        """Test the Taxon endpoint."""
        client_ = Client()
        services_ = [TaxonService.OVERVIEW]
        data_ = client_.taxon(eppo_codes=["BEMITA"], services=services_)
        self.assertIsInstance(data_, dict)

    #############
    # country() #
    #############

    @patch("eppopynder._core._country._country")
    def test_country(self, mock_country):
        """Test the Country endpoint."""
        mock_country.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [CountryService.OVERVIEW]
        data_ = client_.country(iso_codes=["FR"], services=services_)
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_country_online(self):
        """Test the Country endpoint."""
        client_ = Client()
        services_ = [CountryService.OVERVIEW]
        data_ = client_.country(iso_codes=["FR"], services=services_)
        self.assertIsInstance(data_, dict)

    ##########
    # rppo() #
    ##########

    @patch("eppopynder._core._rppo._rppo")
    def test_rppo(self, mock_rppo):
        """Test the RPPO endpoint."""
        mock_rppo.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [RPPOService.OVERVIEW]
        data_ = client_.rppo(rppo_codes=["9A"], services=services_)
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_rppo_online(self):
        """Test the RPPO endpoint."""
        client_ = Client()
        services_ = [RPPOService.OVERVIEW]
        data_ = client_.rppo(rppo_codes=["9A"], services=services_)
        self.assertIsInstance(data_, dict)

    ###########
    # tools() #
    ###########

    @patch("eppopynder._core._tools._tools")
    def test_tools(self, mock_tools):
        """Test the Tools endpoint."""
        mock_tools.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [ToolsService.NAME2CODES]
        data_ = client_.tools(
            services=services_,
            params={ToolsService.NAME2CODES: {"name": "Bemisia tabaci"}}
        )
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_tools_online(self):
        """Test the Tools endpoint."""
        client_ = Client()
        services_ = [ToolsService.NAME2CODES]
        data_ = client_.tools(
            services=services_,
            params={ToolsService.NAME2CODES: {"name": "Bemisia tabaci"}}
        )
        self.assertIsInstance(data_, dict)

    #######################
    # reporting_service() #
    #######################

    @patch("eppopynder._core._reporting_service._reporting_service")
    def test_reporting_service(self, mock_reporting_service):
        """Test the Reporting Service endpoint."""
        mock_reporting_service.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [ReportingServiceService.LIST]
        data_ = client_.reporting_service(services=services_)
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_reporting_service_online(self):
        """Test the Reporting Service endpoint."""
        client_ = Client()
        services_ = [ReportingServiceService.LIST]
        data_ = client_.reporting_service(services=services_)
        self.assertIsInstance(data_, dict)

    ################
    # references() #
    ################

    @patch("eppopynder._core._references._references")
    def test_references(self, mock_references):
        """Test the References endpoint."""
        mock_references.return_value = {}
        client_ = Client(api_key="EPPO_API_KEY")
        services_ = [ReferencesService.Q_LIST]
        data_ = client_.references(services=services_)
        self.assertIsInstance(data_, dict)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test_references_online(self):
        """Test the References endpoint."""
        client_ = Client()
        services_ = [ReferencesService.Q_LIST]
        data_ = client_.references(services=services_)
        self.assertIsInstance(data_, dict)
