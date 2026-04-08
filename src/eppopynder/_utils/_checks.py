"""This module contains internal functions for performing type and data checks.
"""

import pandas as pd


def _require_type(value, expected_type):
    """Check that a value is of the expected type.

    Args:
        value: The value to check.
        expected_type: The expected type.

    Raises:
        TypeError: If the value is not of the expected type.

    Returns:
        None: The function returns nothing if the check passes.
    """

    if not isinstance(value, expected_type):
        raise TypeError(f"Expected type {expected_type}, got {type(value)}")


def _require_trailing_slash(string):
    """Check that a string starts with a trailing slash.

    Args:
        string (str): The string value to check.

    Raises:
        ValueError: If the string is not starting with a trailing slash.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=string, expected_type=str)

    if not string.startswith('/'):
        raise ValueError(f"Expected trailing slash, got {string}")


def _require_list_of(items, expected_type):
    """Check that a list contains only elements of the expected type.

    Args:
        items (list): The list to check.
        expected_type (type): The expected type of the elements.

    Raises:
        TypeError: If at least one element of the list is not of the expected
            type.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=items, expected_type=list)
    _require_type(value=expected_type, expected_type=type)

    for item_ in items:
        if not isinstance(item_, expected_type):
            raise TypeError(f"Expected list of {expected_type}")


def _check_services(services, choices):
    """Validate service names against a set of allowed choices.

    This function checks whether all elements in `services` are included in the
    allowed `choices`. If any unsupported services are found, the function
    raises an informative exception.

    Args:
        services (list): A list of service names to validate.
        choices (list): A list containing the allowed service names.

    Raises:
        ValueError: If any unsupported services are found.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=services, expected_type=list)
    _require_list_of(items=services, expected_type=type(choices[0]))
    _require_type(value=choices, expected_type=list)

    invalid_services_ = set(services) - set(choices)

    if len(invalid_services_) > 0:
        raise ValueError("Unsupported services requested: "
                         + f"{", ".join(invalid_services_)}")


def _require_column_names(dataframe, column_names):
    """Check if a dataframe contains the specified column names.

    This function checks whether a dataframe contains the specified column
    names. If the condition is not verified, the function raises an informative
    exception.

    Args:
        dataframe (pd.DataFrame): The dataframe to validate.
        column_names (list): The list of required column names.

    Raises:
        ValueError: If the required column names are not present in the
            dataframe.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=dataframe, expected_type=pd.DataFrame)
    _require_type(value=column_names, expected_type=list)

    if not all(column_ in dataframe.columns for column_ in column_names):
        raise ValueError("Missing required columns in dataframe: "
                         + f"{", ".join(column_names)}")


def _require_not_all_nan(dataframe, column_name):
    """Check if a dataframe contains the specified column names.

    This function checks whether a dataframe contains the specified column
    names. If the condition is not verified, the function raises an informative
    exception.

    Args:
        dataframe (pd.DataFrame): The dataframe to check.
        column_name (str): The name of the column to check.

    Raises:
        ValueError: If the specified column contains only NaN values.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=dataframe, expected_type=pd.DataFrame)
    _require_type(value=column_name, expected_type=str)

    if (not column_name in dataframe.columns
        or not dataframe[column_name].notna().any()):
        raise ValueError(f"Column {column_name} must contain at least a "
                         + "non-NaN value.")
