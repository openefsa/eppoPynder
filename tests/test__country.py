import os
import unittest
from unittest.mock import patch
import pandas as pd
from dotenv import load_dotenv
from requests import HTTPError

from eppopynder._core._country import _country, CountryService

load_dotenv()


class TestCountry(unittest.TestCase):

    ##############
    # _country() #
    ##############

    def test__country_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _country, api_key=123, iso_codes=[''],
                          services=list())
        self.assertRaises(TypeError, _country, api_key='', iso_codes=123,
                          services=123)
        self.assertRaises(TypeError, _country, api_key='', iso_codes=[1, 2],
                          services=list())
        self.assertRaises(TypeError, _country, api_key='', iso_codes=[''],
                          services=123)
        self.assertRaises(TypeError, _country, api_key='', iso_codes=[''],
                          services=[1, 2])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__country_output(self, mock_fetch_service):
        """Test the output dict structure."""
        mock_fetch_service.return_value = pd.DataFrame()
        services_ = [CountryService.OVERVIEW]
        data_ = _country(
            api_key="EPPO_API_KEY",
            iso_codes=["FR"],
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[CountryService.OVERVIEW], pd.DataFrame)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__country_output_online(self):
        """Test the output dict structure."""
        services_ = [CountryService.OVERVIEW]
        data_ = _country(
            api_key=os.getenv("EPPO_API_KEY"),
            iso_codes=["FR"],
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[CountryService.OVERVIEW], pd.DataFrame)

    @patch("eppopynder._utils._requests._fetch_service")
    def test__country_invalid_iso(self, mock_fetch_service):
        """Test the behaviour for invalid ISO codes."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _country,
                          api_key="EPPO_API_KEY",
                          iso_codes=["BAD_ISO_CODE"])

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__country_invalid_iso_online(self):
        """Test the behaviour for invalid ISO codes."""
        self.assertRaises(HTTPError, _country,
                          api_key=os.getenv("EPPO_API_KEY"),
                          iso_codes=["BAD_ISO_CODE"])

    def test__country_invalid_service(self):
        """Test the behaviour for invalid services."""
        self.assertRaises(TypeError, _country,
                          api_key="EPPO_API_KEY",
                          iso_codes=["FR"], services=["badService"])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__country_invalid_key(self, mock_fetch_service):
        """Test the behaviour for invalid API keys."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _country, api_key="BAD_API_KEY",
                          iso_codes=["FR"])
        mock_fetch_service.side_effect = TypeError
        self.assertRaises(TypeError, _country, api_key=None, iso_codes=["FR"])

    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__country_invalid_key_online(self):
        """Test the behaviour for invalid API keys."""
        self.assertRaises(HTTPError, _country, api_key="BAD_API_KEY",
                          iso_codes=["FR"])
        self.assertRaises(TypeError, _country,
                          api_key=os.getenv("BAD_API_KEY"), iso_codes=["FR"])
