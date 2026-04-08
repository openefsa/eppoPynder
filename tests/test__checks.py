import unittest
import pandas as pd

from eppopynder._utils._checks import (_require_type, _require_trailing_slash,
                                       _require_list_of, _check_services,
                                       _require_column_names,
                                       _require_not_all_nan)


class TestChecks(unittest.TestCase):

    ###################
    # _require_type() #
    ###################

    def test__require_type_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _require_type, value=123,
                          expected_type=str)

    def test__require_type_output(self):
        """Test the behaviour for valid data."""
        self.assertIsNone(_require_type(value=123, expected_type=int))

    #############################
    # _require_trailing_slash() #
    #############################

    def test__require_trailing_slash_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _require_trailing_slash, string=123)

    def test__require_trailing_slash_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(ValueError, _require_trailing_slash, string="country")

    def test__require_trailing_slash_output(self):
        """Test the behaviour for valid data."""
        self.assertIsNone(_require_trailing_slash(string="/country"))

    ######################
    # _require_list_of() #
    ######################

    def test__require_list_of_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _require_list_of, items=123,
                          expected_type=int)
        self.assertRaises(TypeError, _require_list_of, items=list(),
                          expected_type=123)

    def test__require_list_of_invalid(self):
        """Test the behaviour for invalid elements."""
        self.assertRaises(TypeError, _require_list_of, items=[1, 2, 'x'],
                          expected_type=int)

    def test__require_list_of_output(self):
        """Test the output for valid elements."""
        self.assertIsNone(_require_list_of(items=[1, 2, 3], expected_type=int))

    #####################
    # _check_services() #
    #####################

    def test__check_services_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _check_services, services=123,
                          choices=list())
        self.assertRaises(TypeError, _check_services, services=list(),
                          choices=123)
        self.assertRaises(TypeError, _check_services, services=[1, 2],
                          choices=['x', 'y'])

    def test__check_services_invalid(self):
        """Test the behaviour for invalid element types."""
        self.assertRaises(ValueError, _check_services, services=['x', 'a'],
                          choices=['x', 'y'])

    def test__check_services_output(self):
        """Test the output for valid elements."""
        self.assertIsNone(_check_services(
            services=['a', 'b'],
            choices=['a', 'b', 'c']
        ))

    ###########################
    # _require_column_names() #
    ###########################

    def test__require_column_names_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _require_column_names, dataframe=123,
                          column_names=list())
        self.assertRaises(TypeError, _require_column_names,
                          dataframe=pd.DataFrame(), column_names=123)

    def test__require_column_names_invalid(self):
        """Test the behaviour for invalid element types."""
        self.assertRaises(ValueError, _require_column_names,
                          dataframe=pd.DataFrame(), column_names=["column_a"])

    def test__require_column_names_output(self):
        """Test the output for valid elements."""
        self.assertIsNone(_require_column_names(
            dataframe=pd.DataFrame({"column_a": [1, 2, 3]}),
            column_names=["column_a"]
        ))

    ##########################
    # _require_not_all_nan() #
    ##########################

    def test__require_not_all_nan_types(self):
        """Test the behaviour for invalid parameters."""
        self.assertRaises(TypeError, _require_not_all_nan, dataframe=123,
                          column_name="")
        self.assertRaises(TypeError, _require_not_all_nan,
                          dataframe=pd.DataFrame(), column_names=123)

    def test__require_not_all_nan_invalid(self):
        """Test the behaviour for invalid element types."""
        self.assertRaises(ValueError, _require_not_all_nan,
                          dataframe=pd.DataFrame({
                              "column_a": [None, None, None]}),
                          column_name="column_a")

    def test__require_not_all_nan_output(self):
        """Test the output for valid elements."""
        self.assertIsNone(_require_not_all_nan(
            dataframe=pd.DataFrame({"column_a": [1, None, 1]}),
            column_name="column_a"
        ))
