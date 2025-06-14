"""
Module to provide for a manner to load an ApplicationProperties object from a ini-type config file.
"""

import configparser
import os
from typing import Callable, Optional, Set, Tuple

from application_properties.application_properties import ApplicationProperties
from application_properties.application_properties_loader_helper import (
    ApplicationPropertiesLoaderHelper,
)


# pylint: disable=too-few-public-methods
class ApplicationPropertiesConfigLoader:
    """
    Class to provide for a manner to load an ApplicationProperties object from a ini-type config file.
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
        handle_error_fn = (
            ApplicationPropertiesLoaderHelper.set_error_handler_if_not_set(
                handle_error_fn
            )
        )
        (
            did_succeed,
            did_have_one_error,
        ) = ApplicationPropertiesConfigLoader.__check_for_file(
            configuration_file, check_for_file_presence, handle_error_fn
        )
        if not did_succeed:
            return did_succeed, did_have_one_error

        if clear_property_map:
            properties_object.clear()

        config_parser = ApplicationPropertiesConfigLoader.__read_configuration(
            configuration_file, handle_error_fn
        )
        if not config_parser:
            return False, True

        did_apply_one = False
        set_property_names: Set[str] = set()
        for next_section_name in config_parser.sections():
            (
                did_apply_one,
                did_have_one_error,
            ) = ApplicationPropertiesConfigLoader.__next_section(
                properties_object,
                next_section_name,
                configuration_file,
                handle_error_fn,
                section_header,
                config_parser,
                set_property_names,
                did_have_one_error,
                did_apply_one,
            )
        return did_apply_one and not did_have_one_error, did_have_one_error

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __next_section(
        properties_object: ApplicationProperties,
        next_section_name: str,
        configuration_file: str,
        handle_error_fn: Callable[[str, Optional[Exception]], None],
        section_header: Optional[str],
        config_parser: configparser.ConfigParser,
        set_property_names: Set[str],
        did_have_one_error: bool,
        did_apply_one: bool,
    ) -> Tuple[bool, bool]:
        if not ApplicationPropertiesConfigLoader.__verify_section_name(
            properties_object, next_section_name, configuration_file, handle_error_fn
        ):
            did_have_one_error = True
        elif not (section_header and next_section_name != section_header):
            for item_pair in config_parser.items(next_section_name):
                if ApplicationPropertiesConfigLoader.__set_item(
                    properties_object,
                    set_property_names,
                    item_pair,
                    configuration_file,
                    handle_error_fn,
                    section_header,
                    next_section_name,
                ):
                    did_apply_one = True
                else:
                    did_have_one_error = True
                    break
        return did_apply_one, did_have_one_error

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __set_item(
        properties_object: ApplicationProperties,
        set_property_names: Set[str],
        item_pair: Tuple[str, str],
        configuration_file: str,
        handle_error_fn: Callable[[str, Optional[Exception]], None],
        section_header: Optional[str],
        next_section_name: str,
    ) -> bool:
        item_name = item_pair[0]
        item_value = item_pair[1]
        try:
            properties_object.verify_full_key_form(item_name, "Configuration item name")
        except ValueError as this_exception:
            formatted_error = (
                f"Configuration item name '{item_name}' in file '{configuration_file}' "
                + f"is not a valid section name: {str(this_exception)}"
            )
            handle_error_fn(formatted_error, this_exception)
            return False

        full_property_name = (
            f"{item_name}" if section_header else f"{next_section_name}.{item_name}"
        )
        if not item_value.strip():
            formatted_error = f"Full configuration item name '{full_property_name}' in file '{configuration_file}' does not have a value assigned to it."
            handle_error_fn(formatted_error, None)
            return False

        if full_property_name in set_property_names:
            formatted_error = f"Full configuration item name '{full_property_name}' in file '{configuration_file}' occurs multiple times using different formats."
            handle_error_fn(formatted_error, None)
            return False

        full_property = f"{full_property_name}={item_value}"
        properties_object.set_manual_property(full_property)
        set_property_names.add(full_property_name)
        return True

    # pylint: enable=too-many-arguments

    @staticmethod
    def __read_configuration(
        configuration_file: str,
        handle_error_fn: Callable[[str, Optional[Exception]], None],
    ) -> Optional[configparser.ConfigParser]:
        config_parser = configparser.ConfigParser(allow_no_value=False)
        try:
            config_parser.read(configuration_file)
            return config_parser
        except configparser.Error as this_exception:
            formatted_error = (
                f"Specified configuration file '{configuration_file}' "
                + f"is not a valid config file: {str(this_exception)}."
            )
            handle_error_fn(formatted_error, this_exception)
            return None

    @staticmethod
    def __check_for_file(
        configuration_file: str,
        check_for_file_presence: bool,
        handle_error_fn: Callable[[str, Optional[Exception]], None],
    ) -> Tuple[bool, bool]:
        if not os.path.exists(configuration_file) or not os.path.isfile(
            configuration_file
        ):
            if check_for_file_presence:
                return False, False

            formatted_error = (
                f"Specified configuration file '{configuration_file}' does not exist."
            )
            handle_error_fn(formatted_error, None)
            return False, True
        return True, False

    @staticmethod
    def __verify_section_name(
        properties_object: ApplicationProperties,
        next_section_name: str,
        configuration_file: str,
        handle_error_fn: Callable[[str, Optional[Exception]], None],
    ) -> bool:
        try:
            properties_object.verify_full_key_form(
                next_section_name, "Configuration section name"
            )
        except ValueError as this_exception:
            formatted_error = (
                f"Configuration section name '{next_section_name}' in file '{configuration_file}' "
                + f"is not a valid section name: {str(this_exception)}"
            )
            handle_error_fn(formatted_error, this_exception)
            return False
        return True


# pylint: enable=too-few-public-methods
