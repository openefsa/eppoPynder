import os
import unittest
from unittest.mock import patch
import pandas as pd
from dotenv import load_dotenv
from requests import HTTPError

from eppopynder._core._taxon import _taxon, TaxonService

load_dotenv()


class TestTaxon(unittest.TestCase):

    #############
    # _taxon() #
    #############

    def test__taxon_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _taxon, api_key=123, eppo_codes=[''],
                          services=list())
        self.assertRaises(TypeError, _taxon, api_key='', eppo_codes=123,
                          services=123)
        self.assertRaises(TypeError, _taxon, api_key='', eppo_codes=[1, 2],
                          services=list())
        self.assertRaises(TypeError, _taxon, api_key='', eppo_codes=[''],
                          services=123)
        self.assertRaises(TypeError, _taxon, api_key='', eppo_codes=[''],
                          services=[1, 2])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__taxon_output(self, mock_fetch_service):
        """Test the output dict structure."""
        mock_fetch_service.return_value = pd.DataFrame()
        services_ = [TaxonService.OVERVIEW]
        data_ = _taxon(
            api_key="EPPO_API_KEY",
            eppo_codes=["BEMITA"],
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[TaxonService.OVERVIEW], pd.DataFrame)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__taxon_output_online(self):
        """Test the output dict structure."""
        services_ = [TaxonService.OVERVIEW]
        data_ = _taxon(
            api_key=os.getenv("EPPO_API_KEY"),
            eppo_codes=["BEMITA"],
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[TaxonService.OVERVIEW], pd.DataFrame)

    @patch("eppopynder._utils._requests._fetch_service")
    def test__taxon_invalid_eppo(self, mock_fetch_service):
        """Test the behaviour for invalid EPPO codes."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _taxon, api_key="EPPO_API_KEY",
                          eppo_codes=["BAD_EPPO_CODE"])

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__taxon_invalid_eppo_online(self):
        """Test the behaviour for invalid EPPO codes."""
        self.assertRaises(HTTPError, _taxon, api_key=os.getenv("EPPO_API_KEY"),
                          eppo_codes=["BAD_EPPO_CODE"])

    def test__taxon_invalid_service(self):
        """Test the behaviour for invalid services."""
        self.assertRaises(TypeError, _taxon, api_key="EPPO_API_KEY",
                          eppo_codes=["BEMITA"], services=["badService"])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__taxons_invalid_key(self, mock_fetch_service):
        """Test the behaviour for invalid API keys."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _taxon, api_key="BAD_API_KEY",
                          eppo_codes=["BEMITA"])
        mock_fetch_service.side_effect = TypeError
        self.assertRaises(TypeError, _taxon, api_key=None,
                          eppo_codes=["BEMITA"])

    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__taxons_invalid_key_online(self):
        """Test the behaviour for invalid API keys."""
        self.assertRaises(HTTPError, _taxon, api_key="BAD_API_KEY",
                          eppo_codes=["BEMITA"])
        self.assertRaises(TypeError, _taxon, api_key=os.getenv("BAD_API_KEY"),
                          eppo_codes=["BEMITA"])
