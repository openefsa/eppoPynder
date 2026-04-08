import os
import unittest
from unittest.mock import patch
import pandas as pd
from dotenv import load_dotenv
from requests import HTTPError

from eppopynder._core._reporting_service import (_reporting_service,
                                                 ReportingServiceService)

load_dotenv()


class TestReportingService(unittest.TestCase):

    ########################
    # _reporting_service() #
    ########################

    def test__reporting_service_types(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _reporting_service, api_key=123,
                          services=list(), params=dict())
        self.assertRaises(TypeError, _reporting_service, api_key='',
                          services=123, params=dict())
        self.assertRaises(TypeError, _reporting_service, api_key='',
                          services=list(), params=123)

    @patch("eppopynder._utils._requests._fetch_service")
    def test__reporting_service_output(self, mock_fetch_service):
        """Test the output dict structure."""
        mock_fetch_service.return_value = pd.DataFrame()
        services_ = [ReportingServiceService.LIST]
        data_ = _reporting_service(
            api_key="EPPO_API_KEY",
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(
            data_[ReportingServiceService.LIST],
            pd.DataFrame
        )

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__reporting_service_output_online(self):
        """Test the output dict structure."""
        services_ = [ReportingServiceService.LIST]
        data_ = _reporting_service(
            api_key=os.getenv("EPPO_API_KEY"),
            services=services_
        )
        self.assertIsInstance(data_, dict)
        self.assertEqual(list(data_.keys()), services_)
        self.assertIsInstance(
            data_[ReportingServiceService.LIST],
            pd.DataFrame
        )

    @patch("eppopynder._utils._requests._fetch_service")
    def test__reporting_service_invalid_param(self, mock_fetch_service):
        """Test the behaviour for invalid request parameters."""
        mock_fetch_service.side_effect = ValueError
        self.assertRaises(ValueError, _reporting_service,
                          api_key="EPPO_API_KEY",
                          params={ReportingServiceService.REPORTING: {
                              "bad_param": 234
                          }})

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__reporting_service_invalid_param_online(self):
        """Test the behaviour for invalid request parameters."""
        self.assertRaises(ValueError, _reporting_service,
                          api_key=os.getenv("EPPO_API_KEY"),
                          params={ReportingServiceService.REPORTING: {
                              "bad_param": 234
                          }})

    def test__reporting_service_invalid_service(self):
        """Test the behaviour for invalid services."""
        self.assertRaises(TypeError, _reporting_service,
                          api_key="EPPO_API_KEY",
                          services=["badService"])

    @patch("eppopynder._utils._requests._fetch_service")
    def test__reporting_service_invalid_key(self, mock_fetch_service):
        """Test the behaviour for invalid API keys."""
        mock_fetch_service.side_effect = HTTPError
        self.assertRaises(HTTPError, _reporting_service, api_key="BAD_API_KEY",
                          services=[ReportingServiceService.LIST])
        mock_fetch_service.side_effect = TypeError
        self.assertRaises(TypeError, _reporting_service, api_key=None,
                          services=[ReportingServiceService.LIST])

    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__reporting_service_invalid_key_online(self):
        """Test the behaviour for invalid API keys."""
        self.assertRaises(HTTPError, _reporting_service, api_key="BAD_API_KEY",
                          services=[ReportingServiceService.LIST])
        self.assertRaises(TypeError, _reporting_service,
                          api_key=os.getenv("BAD_API_KEY"),
                          services=[ReportingServiceService.LIST])
