import os
import unittest
from unittest.mock import patch
import pandas as pd
from dotenv import load_dotenv
from requests import HTTPError

from eppopynder._core._tools import _tools, ToolsService

load_dotenv()


class TestTools(unittest.TestCase):

    ############
    # _tools() #
    ############

    def test__tools_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _tools, api_key=123, services=list(),
                          params=dict())
        self.assertRaises(TypeError, _tools, api_key='', services=123,
                          params=dict())
        self.assertRaises(TypeError, _tools, api_key='', services=list(),
                          params=123)

    @patch("eppopynder._utils._requests._fetch_service")
    def test__tools_output(self, mock_fetch_service):
        """Test the output dict structure."""
        mock_fetch_service.return_value = pd.DataFrame()
        services_ = [ToolsService.NAME2CODES]
        data_ = _tools(
            api_key="EPPO_API_KEY",
            services=services_,
            params={ToolsService.NAME2CODES: {"name": "Bemisia tabaci"}}
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[ToolsService.NAME2CODES], pd.DataFrame)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__tools_output_online(self):
        """Test the output dict structure."""
        services_ = [ToolsService.NAME2CODES]
        data_ = _tools(
            api_key=os.getenv("EPPO_API_KEY"),
            services=services_,
            params={ToolsService.NAME2CODES: {"name": "Bemisia tabaci"}}
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(data_[ToolsService.NAME2CODES], pd.DataFrame)

    @patch("eppopynder._utils._requests._fetch_service")
    def test__tools_invalid_param(self, mock_fetch_service):
        """Test the behaviour for invalid parameters."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _tools, api_key="EPPO_API_KEY",
                          params={"name2codes": {"onlyPreferred": False}})

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__tools_invalid_param_online(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(HTTPError, _tools, api_key=os.getenv("EPPO_API_KEY"),
                          params={"name2codes": {"onlyPreferred": False}})

    def test__tools_invalid_service(self):
        """Test the behaviour for invalid services."""
        self.assertRaises(TypeError, _tools, api_key="EPPO_API_KEY",
                          services=["badService"])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__tools_invalid_key(self, mock_fetch_service):
        """Test the behaviour for invalid API keys."""
        params_ = {"name2codes": {"name": "Bemisia tabaci"}}
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _tools, api_key="BAD_API_KEY",
                          params=params_)
        mock_fetch_service.side_effect = TypeError
        self.assertRaises(TypeError, _tools, api_key=None, params=params_)

    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__tools_invalid_key_online(self):
        """Test the behaviour for invalid API keys."""
        params_ = {"name2codes": {"name": "Bemisia tabaci"}}
        self.assertRaises(HTTPError, _tools, api_key="BAD_API_KEY",
                          params=params_)
        self.assertRaises(TypeError, _tools, api_key=os.getenv("BAD_API_KEY"),
                          params=params_)
