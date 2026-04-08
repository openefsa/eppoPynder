import os
import json
import unittest
from unittest.mock import patch
import pandas as pd
import requests.exceptions
from dotenv import load_dotenv
from json import JSONDecodeError
from requests import Response, HTTPError

from eppopynder._utils._requests import (_build_endpoint, _perform_request,
                                         _handle_http_errors, _parse_response,
                                         _enrich_response, _query,
                                         _fetch_service,
                                         _build_reporting_service_path)

load_dotenv()


class TestRequests(unittest.TestCase):

    #####################
    # _build_endpoint() #
    #####################

    def test__build_endpoint_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _build_endpoint, base_path=123, code='',
                          service='')
        self.assertRaises(ValueError, _build_endpoint, base_path="general",
                          code='', service='')
        self.assertRaises(TypeError, _build_endpoint, base_path="/general",
                          code=123, service='')
        self.assertRaises(TypeError, _build_endpoint, base_path="/general",
                          code='', service=123)

    def test__build_endpoint_output1(self):
        """Test the behaviour if only the base path is given."""
        self.assertEqual(
            _build_endpoint(base_path="/taxons/taxon"),
            "/taxons/taxon"
        )

    def test__build_endpoint_output2(self):
        """Test the behaviour if a resource identifier is given."""
        self.assertEqual(
            _build_endpoint(base_path="/taxon/taxon", code="BEMITA"),
            "/taxon/taxon/BEMITA"
        )

    def test__build_endpoint_output3(self):
        """Test the behaviour if a service is given."""
        self.assertEqual(
            _build_endpoint(
                base_path="/country",
                code="FR",
                service="overview"
            ),
            "/country/FR/overview"
        )

    def test__build_endpoint_output4(self):
        """Test the behaviour if no resource identifier is given."""
        self.assertEqual(
            _build_endpoint(base_path="/reportings", service="list"),
            "/reportings/list"
        )

    ###################################
    # _build_reporting_service_path() #
    ###################################

    def test__build_reporting_service_path_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _build_reporting_service_path,
                          service=123, params=dict())
        self.assertRaises(TypeError, _build_reporting_service_path, service='',
                          params=123)

    def test__build_reporting_service_path_output1(self):
        """Test the behaviour for valid parameters."""
        self.assertEqual(
            _build_reporting_service_path(
                service="reporting",
                params={"reporting_id": 234}),
            "reporting/234"
        )
        self.assertEqual(
            _build_reporting_service_path(
                service="article",
                params={"article_id": 234}),
            "article/234"
        )

    def test__build_reporting_service_path_output3(self):
        """Test the behaviour for services without parameters."""
        self.assertEqual(
            _build_reporting_service_path(
                service="list",
                params=dict()),
            "list"
        )

    def test__build_reporting_service_path_invalid(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(ValueError, _build_reporting_service_path,
                          service="reporting", params={'a': 10})
        self.assertRaises(ValueError, _build_reporting_service_path,
                          service="article", params={'a': 234})

    ######################
    # _perform_request() #
    ######################

    def test__perform_request_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _perform_request, url=123, api_key='',
                          params=None)
        self.assertRaises(TypeError, _perform_request,
                          url="https://example.org", api_key=123,
                          params=None)
        self.assertRaises(TypeError, _perform_request,
                          url="https://example.org", api_key='', params=123)

    @patch("eppopynder._utils._requests.requests.get")
    def test__perform_request_malformed(self, mock_get):
        """Test the behaviour for malformed requests."""
        mock_get.side_effect = requests.exceptions.ConnectionError
        self.assertRaises(Exception, _perform_request,
                          url="https://invalid-domain", api_key="EPPO_API_KEY")

    # This test performs real requests.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_request_malformed_online(self):
        """Test the behaviour for malformed requests."""
        self.assertRaises(Exception, _perform_request,
                          url="https://invalid-domain", api_key="EPPO_API_KEY")

    @patch("eppopynder._utils._requests.requests.get")
    def test__perform_request_output(self, mock_get):
        """Test the output type of the request."""
        mock_get.return_value = Response()
        response_ = _perform_request(
            url="https://api.eppo.int/gd/v2/taxons/taxon/BEMITA/overview",
            api_key="EPPO_API_KEY"
        )
        self.assertIsInstance(response_, Response)

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__perform_request_output_online(self):
        """Test the output type of the request."""
        response_ = _perform_request(
            url="https://api.eppo.int/gd/v2/taxons/taxon/BEMITA/overview",
            api_key=os.getenv("EPPO_API_KEY")
        )
        self.assertIsInstance(response_, Response)

    #########################
    # _handle_http_errors() #
    #########################

    def test__handle_http_errors_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _handle_http_errors, response=123)

    def test__handle_http_errors_valid(self):
        """Test the behaviour for status code 200."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://api.eppo.int/gd/v2/status"
        response_.method = "GET"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"data": "Custom data"})
                              .encode("utf-8"))
        self.assertIsNone(_handle_http_errors(response=response_))

    def test__handle_http_errors_handled(self):
        """Test the behaviour for handled status codes."""
        response_ = Response()
        response_.status_code = 403
        response_.url = "https://api.eppo.int/gd/v2/status"
        response_.method = "GET"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"error": "Custom message"})
                              .encode("utf-8"))
        self.assertRaises(HTTPError, _handle_http_errors, response=response_)

    def test__handle_http_errors_handled_invalid(self):
        """Test the behaviour for handled status codes."""
        response_ = Response()
        response_.status_code = 403
        response_.url = "https://api.eppo.int/gd/v2/status"
        response_.method = "GET"
        response_.headers["Content-Type"] = "text/html"
        response_._content = "<html>content</html>".encode("utf-8")
        self.assertRaises(
            HTTPError,
            _handle_http_errors,
            response=response_
        )

    def test__handle_http_errors_invalid(self):
        """Test the behaviour for bad status codes."""
        response_ = Response()
        response_.status_code = 502
        response_.url = "https://api.eppo.int/gd/v2/status"
        response_.method = "GET"
        self.assertRaises(HTTPError, _handle_http_errors, response=response_)

    #####################
    # _parse_response() #
    #####################

    def test__parse_response_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _parse_response, response=123)

    def test__parse_response_valid(self):
        """Test the behaviour for valid parameters and data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://api.eppo.int/gd/v2/status"
        response_.method = "GET"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"data": "Custom data"})
                              .encode("utf-8"))
        self.assertIsInstance(
            _parse_response(response=response_),
            pd.DataFrame
        )

    def test__parse_response_invalid(self):
        """Test the behaviour for invalid body data."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://api.eppo.int/gd/v2/status"
        response_.method = "GET"
        response_.headers["Content-Type"] = "text/html"
        response_._content = "<html>content</html>".encode("utf-8")
        self.assertRaises(
            JSONDecodeError,
            _parse_response,
            response=response_
        )

    ######################
    # _enrich_response() #
    ######################

    def test__enrich_response_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _enrich_response, response_data=123,
                          url='')
        self.assertRaises(TypeError, _enrich_response,
                          response_data=pd.DataFrame(), url=123)

    def test__enrich_response_valid(self):
        """Test the behaviour for valid parameters."""
        data_ = _enrich_response(
            response_data=pd.DataFrame({"data": ["Custom data"]}),
            url="https://example.org"
        )
        self.assertTrue("queried_on" in data_)
        self.assertTrue("queried_url" in data_)
        self.assertEqual(data_["queried_url"].iloc[0],
                         "https://example.org")

    ############
    # _query() #
    ############

    def test__query_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _query, endpoint=123, api_key='',
                          params=dict())
        self.assertRaises(ValueError, _query, endpoint="general", api_key='',
                          params=dict())
        self.assertRaises(TypeError, _query, endpoint="/general", api_key=123,
                          params=dict())
        self.assertRaises(TypeError, _query, endpoint="/general", api_key='',
                          params=123)

    @patch("eppopynder._utils._requests._perform_request")
    def test__query_wrong_endpoint(self, mock_perform_request):
        """Test the behaviour if a bad endpoint is given."""
        mock_perform_request.side_effect = HTTPError
        self.assertRaises(HTTPError, _query,
                          endpoint="/taxons/taxon/BEMITA/badService",
                          api_key="EPPO_API_KEY")

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__query_wrong_endpoint_online(self):
        """Test the behaviour if a bad endpoint is given."""
        self.assertRaises(HTTPError, _query,
                          endpoint="/taxons/taxon/BEMITA/badService",
                          api_key=os.getenv("EPPO_API_KEY"))

    @patch("eppopynder._utils._requests._perform_request")
    def test__query_wrong_api_key(self, mock_perform_request):
        """Test the behaviour if a bad API key is given."""
        mock_perform_request.side_effect = HTTPError
        self.assertRaises(HTTPError, _query,
                          endpoint="/taxons/taxon/BEMITA/overview",
                          api_key="BAD_API_KEY")

    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__query_wrong_api_key_online(self):
        """Test the behaviour if a bad API key is given."""
        self.assertRaises(HTTPError, _query,
                          endpoint="/taxons/taxon/BEMITA/overview",
                          api_key="BAD_API_KEY")

    @patch("eppopynder._utils._requests._perform_request")
    def test__query_valid(self, mock_perform_request):
        """Test the behaviour for valid parameters."""
        response_ = Response()
        response_.status_code = 200
        response_.url = "https://api.eppo.int/gd/v2/status"
        response_.method = "GET"
        response_.headers["Content-Type"] = "application/json"
        response_._content = (json.dumps({"data": "Custom data"})
                              .encode("utf-8"))
        mock_perform_request.return_value = response_
        self.assertIsInstance(
            _query(
                endpoint="/status",
                api_key="EPPO_API_KEY"
            ),
            pd.DataFrame
        )

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__query_valid_online(self):
        """Test the behaviour for valid parameters."""
        self.assertIsInstance(
            _query(
                endpoint="/taxons/taxon/BEMITA/overview",
                api_key=os.getenv("EPPO_API_KEY")
            ),
            pd.DataFrame
        )

    ####################
    # _fetch_service() #
    ####################

    def test__fetch_service_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _fetch_service, base_path=123, api_key='',
                          code='', service='', params=dict())
        self.assertRaises(ValueError, _fetch_service, base_path="taxons/taxon",
                          api_key='', code='', service='', params=dict())
        self.assertRaises(TypeError, _fetch_service, base_path="/taxons/taxon",
                          api_key=123, code='', service='', params=dict())
        self.assertRaises(TypeError, _fetch_service, base_path="/taxons/taxon",
                          api_key='', code=123, service='', params=dict())
        self.assertRaises(TypeError, _fetch_service, base_path="/taxons/taxon",
                          api_key='', code='', service=123, params=dict())
        self.assertRaises(TypeError, _fetch_service, base_path="/taxons/taxon",
                          api_key='', code='', service='', params=123
        )

    @patch("eppopynder._utils._requests._query")
    def test__fetch_service_output(self, mock_query):
        """Test the output type for valid parameters."""
        mock_query.return_value = pd.DataFrame({'a': [1]})
        self.assertIsInstance(
            _fetch_service(
                base_path="/taxons/taxon",
                api_key="EPPO_API_KEY",
                code="BEMITA",
                service="overview"
            ),
            pd.DataFrame
        )

    # This test requires the EPPO_API_KEY environment variable to be set.
    # This test performs real requests to the EPPO API.
    @unittest.skipIf(os.getenv("SKIP_ONLINE_TESTS") == "true",
                     "Skip online tests")
    def test__fetch_service_output_online(self):
        """Test the output type for valid parameters."""
        self.assertIsInstance(
            _fetch_service(
                base_path="/taxons/taxon",
                api_key=os.getenv("EPPO_API_KEY"),
                code="BEMITA",
                service="overview"
            ),
            pd.DataFrame
        )
