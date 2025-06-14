"""
Module to provide for a manner to load an ApplicationProperties object from a TOML file.
"""

import os
from typing import Any, Callable, Dict, Optional, Tuple

import tomli

from application_properties.application_properties import ApplicationProperties
from application_properties.application_properties_loader_helper import (
    ApplicationPropertiesLoaderHelper,
)


# pylint: disable=too-few-public-methods
class ApplicationPropertiesTomlLoader:
    """
    Class to provide for a manner to load an ApplicationProperties object from a TOML file.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def load_and_set(
        properties_object: ApplicationProperties,
        configuration_file: str,
        section_header: Optional[str] = None,
        handle_error_fn: Optional[Callable[[str, Optional[Exception]], None]] = None,
        clear_property_map: bool = True,
        check_for_file_presence: bool = True,
    ) -> Tuple[bool, bool]:
        """
        Load the specified file and set it into the given properties object.
        """
        if check_for_file_presence and not (
            os.path.exists(configuration_file) and os.path.isfile(configuration_file)
        ):
            return False, False

        handle_error_fn = (
            ApplicationPropertiesLoaderHelper.set_error_handler_if_not_set(
                handle_error_fn
            )
        )

        did_have_one_error = False
        configuration_map: Optional[Dict[str, Any]] = {}
        try:
            with open(configuration_file, "rb") as infile:
                configuration_map = tomli.load(infile)
        except tomli.TOMLDecodeError as this_exception:
            formatted_error = (
                f"Specified configuration file '{configuration_file}' "
                + f"is not a valid TOML file: {str(this_exception)}."
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
        if not did_have_one_error:
            if configuration_map and section_header:
                configuration_map = (
                    ApplicationPropertiesTomlLoader.__apply_section_header(
                        configuration_map, section_header
                    )
                )
            if configuration_map:
                properties_object.load_from_dict(
                    configuration_map, clear_map=clear_property_map
                )
                did_apply_map = True
        return did_apply_map and not did_have_one_error, did_have_one_error

    # pylint: enable=too-many-arguments

    @staticmethod
    def __apply_section_header(
        configuration_map: Dict[str, Any], section_header: str
    ) -> Optional[Dict[str, Any]]:
        for next_header_part in section_header.split("."):
            if next_header_part not in configuration_map:
                return None
            configuration_map = configuration_map[next_header_part]
            if not isinstance(configuration_map, dict):
                return None

        return configuration_map


# pylint: enable=too-few-public-methods
