"""
Module to provide for a manner to load an ApplicationProperties object from a JSON file.
"""

import json
import os
from typing import Any, Callable, Dict, Optional, Tuple

from application_properties.application_properties import ApplicationProperties
from application_properties.application_properties_loader_helper import (
    ApplicationPropertiesLoaderHelper,
)


# pylint: disable=too-few-public-methods
class ApplicationPropertiesJsonLoader:
    """
    Class to provide for a manner to load an ApplicationProperties object from a JSON file.
    """

    @staticmethod
    def load_and_set(
        properties_object: ApplicationProperties,
        configuration_file: str,
        handle_error_fn: Optional[Callable[[str, Optional[Exception]], None]] = None,
        clear_property_map: bool = True,
        check_for_file_presence: bool = True,
    ) -> Tuple[bool, bool]:
        """
        Load the specified file and set it into the given properties object.
        """
        if check_for_file_presence and (
            not os.path.exists(configuration_file)
            or not os.path.isfile(configuration_file)
        ):
            return False, False

        configuration_map: Dict[Any, Any] = {}
        handle_error_fn = (
            ApplicationPropertiesLoaderHelper.set_error_handler_if_not_set(
                handle_error_fn
            )
        )
        did_have_one_error = False
        try:
            with open(configuration_file, encoding="utf-8") as infile:
                configuration_map = json.load(infile)
        except json.decoder.JSONDecodeError as this_exception:
            formatted_error = (
                f"Specified configuration file '{configuration_file}' "
                + f"is not a valid JSON file: {str(this_exception)}."
            )
            did_have_one_error = True
            handle_error_fn(formatted_error, this_exception)
        except IOError as this_exception:
            formatted_error = (
                f"Specified configuration file '{configuration_file}' "
                + f"was not loaded: {str(this_exception)}."
            )
            did_have_one_error = True
            handle_error_fn(formatted_error, this_exception)

        did_apply_map = False
        if not did_have_one_error and configuration_map:
            try:
                properties_object.load_from_dict(
                    configuration_map, clear_map=clear_property_map
                )
                did_apply_map = True
            except ValueError as this_exception:
                formatted_error = (
                    f"Specified configuration file '{configuration_file}' "
                    + f"is not valid: {str(this_exception)}"
                )
                did_have_one_error = True
                handle_error_fn(formatted_error, this_exception)
        return did_apply_map and not did_have_one_error, did_have_one_error


# pylint: enable=too-few-public-methods
