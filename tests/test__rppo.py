import os
import unittest
from unittest.mock import patch
import pandas as pd
from dotenv import load_dotenv
from requests import HTTPError

from eppopynder._core._rppo import _rppo, RPPOService

load_dotenv()


class TestRPPO(unittest.TestCase):

    ###########
    # _rppo() #
    ###########

    def test__rppo_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _rppo, api_key=123, rppo_codes=[''],
                          services=list())
        self.assertRaises(TypeError, _rppo, api_key='', rppo_codes=123,
                          services=123)
        self.assertRaises(TypeError, _rppo, api_key='', rppo_codes=[1, 2],
                          services=list())
        self.assertRaises(TypeError, _rppo, api_key='', rppo_codes=[''],
                          services=123)
        self.assertRaises(TypeError, _rppo, api_key='', rppo_codes=[''],
                          services=[1, 2])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__rppo_output(self, mock_fetch_service):
        """Test the output dict structure."""
        mock_fetch_service.return_value = pd.DataFrame()
        services_ = [RPPOService.OVERVIEW]
        data_ = _rppo(
            api_key="EPPO_API_KEY",
            rppo_codes=["9A"],
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[RPPOService.OVERVIEW], pd.DataFrame)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__rppo_output_online(self):
        """Test the output dict structure."""
        services_ = [RPPOService.OVERVIEW]
        data_ = _rppo(
            api_key=os.getenv("EPPO_API_KEY"),
            rppo_codes=["9A"],
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[RPPOService.OVERVIEW], pd.DataFrame)

    @patch("eppopynder._utils._requests._fetch_service")
    def test__rppo_invalid_rppo(self, mock_fetch_service):
        """Test the behaviour for invalid RPPO codes."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _rppo, api_key="EPPO_API_KEY",
                          rppo_codes=["BAD_RPPO_CODE"])

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__rppo_invalid_rppo_online(self):
        """Test the behaviour for invalid RPPO codes."""
        self.assertRaises(HTTPError, _rppo,
                          api_key=os.getenv("EPPO_API_KEY"),
                          rppo_codes=["BAD_RPPO_CODE"])

    def test__rppo_invalid_service(self):
        """Test the behaviour for invalid services."""
        self.assertRaises(TypeError, _rppo, api_key="EPPO_API_KEY",
                          rppo_codes=["9A"], services=["badService"])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__rppo_invalid_key(self, mock_fetch_service):
        """Test the behaviour for invalid API keys."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _rppo, api_key="BAD_API_KEY",
                          rppo_codes=["9A"])
        mock_fetch_service.side_effect = TypeError
        self.assertRaises(TypeError, _rppo, api_key=None, rppo_codes=["9A"])

    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__rppo_invalid_key_online(self):
        """Test the behaviour for invalid API keys."""
        self.assertRaises(HTTPError, _rppo, api_key="BAD_API_KEY",
                          rppo_codes=["9A"])
        self.assertRaises(TypeError, _rppo,
                          api_key=os.getenv("BAD_API_KEY"), rppo_codes=["9A"])
