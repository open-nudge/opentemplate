"""
Module that provides for an encapsulation of properties for an application.
"""

import contextlib
import copy
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, cast

LOGGER = logging.getLogger(__name__)


class ApplicationProperties:
    """
    Class that provides for an encapsulation of properties for an application.
    """

    __separator = "."
    __assignment_operator = "="
    __manual_property_type_prefix = "$"
    __manual_property_type_string = "$"
    __manual_property_type_integer = "#"
    __manual_property_type_boolean = "!"

    """
    Class to provide for a container of properties that belong to the application.
    """

    def __init__(
        self, strict_mode: bool = False, convert_untyped_if_possible: bool = False
    ) -> None:
        """
        Initializes an new instance of the ApplicationProperties class.
        """
        self.__flat_property_map: Dict[str, Any] = {}
        self.__strict_mode: bool = strict_mode
        self.__convert_untyped_if_possible: bool = convert_untyped_if_possible

    @property
    def separator(self) -> str:
        """
        Separator used to split the hierarchy of the property names.
        """
        return self.__separator

    @property
    def number_of_properties(self) -> int:
        """
        Number of properties that exist in the map.
        """
        return len(self.property_names)

    @property
    def property_names(self) -> List[str]:
        """
        List of each of the properties in the map.
        """
        return [
            next_item
            for next_item in self.__flat_property_map
            if not next_item.startswith(ApplicationProperties.__separator)
        ]

    @property
    def strict_mode(self) -> bool:
        """
        Gets whether strict mode is on by default.
        """
        return self.__strict_mode

    def enable_strict_mode(self) -> None:
        """
        Sets strict mode to True to enable it.
        """
        self.__strict_mode = True

    @property
    def convert_untyped_if_possible(self) -> bool:
        """
        Gets whether the package is allowed to try and unconvert untyped entries.
        """
        return self.__convert_untyped_if_possible

    def enable_convert_untyped_if_possible(self) -> None:
        """
        Sets convert_untyped_if_possible to True to enable it.
        """
        self.__convert_untyped_if_possible = True

    def clear(self) -> None:
        """
        Clear the configuration map.
        """
        self.__flat_property_map.clear()

    def load_from_dict(
        self, config_map: Dict[Any, Any], clear_map: bool = True
    ) -> None:
        """
        Load the properties from a provided dictionary.
        """

        if not isinstance(config_map, dict):
            raise ValueError("Specified parameter was not a dictionary.")

        LOGGER.debug("Loading from dictionary: {%s}", str(config_map))
        if clear_map:
            self.clear()
        self.__scan_map(config_map, "")

    @staticmethod
    def verify_full_part_form(property_key: str) -> str:
        """
        Given one part of a full key, verify that it is composed properly.
        """

        if (
            " " in property_key
            or "\t" in property_key
            or "\n" in property_key
            or ApplicationProperties.__assignment_operator in property_key
            or ApplicationProperties.__separator in property_key
        ):
            raise ValueError(
                "Each part of the property key cannot contain a whitespace character, "
                + f"a '{ApplicationProperties.__assignment_operator}' character, or "
                + f"a '{ApplicationProperties.__separator}' character."
            )
        if not property_key:
            raise ValueError(
                "Each part of the property key must contain at least one character."
            )
        return property_key

    @staticmethod
    def verify_full_key_form(
        property_key: str, alternate_name: Optional[str] = None
    ) -> str:
        """
        Given a full key, verify that it is composed properly.
        """

        key_name = alternate_name or "Full property key"

        if property_key.startswith(
            ApplicationProperties.__separator
        ) or property_key.endswith(ApplicationProperties.__separator):
            raise ValueError(
                f"{key_name} must not start or end with the '{ApplicationProperties.__separator}' character."
            )
        doubles = (
            f"{ApplicationProperties.__separator}{ApplicationProperties.__separator}"
        )
        doubles_index = property_key.find(doubles)
        if doubles_index != -1:
            raise ValueError(
                f"{key_name} cannot contain multiples of "
                + f"the {ApplicationProperties.__separator} without any text between them."
            )
        split_key = property_key.split(ApplicationProperties.__separator)
        for next_key in split_key:
            ApplicationProperties.verify_full_part_form(next_key)
        return property_key

    @staticmethod
    def verify_manual_property_form(string_to_verify: str) -> str:
        """
        Verify the general form of a manual property string. i.e. key=value
        """

        if not isinstance(string_to_verify, str):
            raise ValueError("Manual property form must be a string.")
        equals_index = string_to_verify.find(
            ApplicationProperties.__assignment_operator
        )
        if equals_index == -1:
            raise ValueError(
                "Manual property key and value must be separated by the '=' character."
            )
        property_key = string_to_verify[:equals_index]
        ApplicationProperties.verify_full_key_form(property_key)
        return string_to_verify

    def set_manual_property(self, combined_string: str) -> None:
        """
        Manually set a property for the object.
        """

        if not isinstance(combined_string, str):
            iterator = None
            try:
                iterator = iter(combined_string)
            except TypeError as this_exception:
                raise ValueError(
                    "Manual property form must either be a string or an iterable of strings."
                ) from this_exception
            for i in iterator:
                self.set_manual_property(i)
            return

        ApplicationProperties.verify_manual_property_form(combined_string)
        equals_index = combined_string.find(ApplicationProperties.__assignment_operator)
        property_key = combined_string[:equals_index].lower()
        property_value = combined_string[equals_index + 1 :]
        composed_property_value: Any = property_value

        if (
            property_value.startswith(
                ApplicationProperties.__manual_property_type_prefix
            )
            and len(property_value) >= 2
        ):
            composed_property_value = self.__adjust_property_type(property_value)

        # This is a bit of a kludge, but it works consistently.  The manually set property
        # is always a string.  If the string has no type information associatede with it,
        # it is eligible for conversion into one of the other types.  To properly denote that
        # the value did not have any type information, it is saved again in the dictionary
        # with a prefix of the separator character, to denote eligibility.
        else:
            self.__flat_property_map[
                f"{ApplicationProperties.__separator}{property_key}"
            ] = property_value

        self.__flat_property_map[property_key] = copy.deepcopy(composed_property_value)
        LOGGER.debug(
            "Adding configuration '%s' : {%s}",
            property_key,
            str(composed_property_value),
        )

    def __adjust_property_type(self, property_value: str) -> Any:
        composed_property_value: Any = None
        if property_value[1] == ApplicationProperties.__manual_property_type_string:
            composed_property_value = property_value[2:]
        elif property_value[1] == ApplicationProperties.__manual_property_type_integer:
            try:
                composed_property_value = int(property_value[2:])
            except ValueError as this_exception:
                raise ValueError(
                    f"Manual property value '{property_value}' cannot be translated into an integer."
                ) from this_exception
        elif property_value[1] == ApplicationProperties.__manual_property_type_boolean:
            composed_property_value = property_value[2:].lower() == "true"
        else:
            composed_property_value = property_value[1:]
        return composed_property_value

    # pylint: disable=unidiomatic-typecheck
    # pylint: disable=too-many-arguments
    def get_property(
        self,
        property_name: str,
        property_type: type,
        default_value: Any = None,
        valid_value_fn: Optional[Callable[[Any], Any]] = None,
        is_required: bool = False,
        strict_mode: Optional[Any] = None,
    ) -> Any:
        """
        Get an property of a generic type from the configuration.
        """

        if strict_mode is None:
            strict_mode = self.__strict_mode

        if not isinstance(property_name, str):
            raise ValueError("The propertyName argument must be a string.")
        ApplicationProperties.verify_full_key_form(property_name)
        if not isinstance(property_type, type):
            raise ValueError(
                f"The property_type argument for '{property_name}' must be a type."
            )
        if default_value is not None and type(default_value) != property_type:
            raise ValueError(
                f"The default value for property '{property_name}' must "
                + f"either be None or a '{property_type.__name__}' value."
            )

        property_value = default_value
        property_name = property_name.lower()
        LOGGER.debug("property_name=%s", property_name)
        if property_name in self.__flat_property_map:
            property_value = self.__get_present_property(
                property_name,
                property_value,
                property_type,
                strict_mode,
                valid_value_fn,
            )
        elif is_required:
            raise ValueError(
                f"A value for property '{property_name}' must be provided."
            )
        return property_value

    # pylint: enable=unidiomatic-typecheck
    # pylint: enable=too-many-arguments

    # pylint: disable=unidiomatic-typecheck
    def __get_present_property_value(
        self, property_name: str, property_type: type
    ) -> Tuple[bool, Any]:
        found_value = self.__flat_property_map[property_name]
        is_eligible = type(found_value) == property_type

        covertable_property_name = f"{ApplicationProperties.__separator}{property_name}"
        if (
            not is_eligible
            and property_type != str
            and self.__convert_untyped_if_possible
            and covertable_property_name in self.__flat_property_map
        ):
            found_value = self.__flat_property_map[covertable_property_name]
            # print(f"::{covertable_property_name}::{found_value}::")
            if property_type == bool:
                found_value = f"{ApplicationProperties.__manual_property_type_prefix}{ApplicationProperties.__manual_property_type_boolean}{found_value}"
            else:
                found_value = f"{ApplicationProperties.__manual_property_type_prefix}{ApplicationProperties.__manual_property_type_integer}{found_value}"
            with contextlib.suppress(ValueError):
                found_value = self.__adjust_property_type(found_value)
                is_eligible = True
            # print(f"::{covertable_property_name}::{found_value}::")
        return is_eligible, found_value

    # pylint: enable=unidiomatic-typecheck

    # pylint: disable=too-many-arguments, broad-exception-caught
    def __get_present_property(
        self,
        property_name: str,
        property_value: Any,
        property_type: type,
        strict_mode: bool,
        valid_value_fn: Optional[Callable[[Any], Any]],
    ) -> Any:
        is_eligible, found_value = self.__get_present_property_value(
            property_name, property_type
        )
        if not is_eligible and strict_mode:
            raise ValueError(
                f"The value for property '{property_name}' must be of type '{property_type.__name__}'."
            )
        if is_eligible and valid_value_fn:
            try:
                valid_value_fn(found_value)
            except Exception as this_exception:
                is_eligible = False
                if strict_mode:
                    raise ValueError(
                        f"The value for property '{property_name}' is not valid: {str(this_exception)}"
                    ) from this_exception
        if is_eligible:
            property_value = found_value
        return property_value

    # pylint: enable=too-many-arguments, broad-exception-caught

    def get_boolean_property(
        self,
        property_name: str,
        default_value: Optional[bool] = None,
        is_required: bool = False,
        strict_mode: Optional[bool] = None,
    ) -> bool:
        """
        Get a boolean property from the configuration.
        """
        return cast(
            bool,
            self.get_property(
                property_name,
                bool,
                default_value=default_value,
                valid_value_fn=None,
                is_required=is_required,
                strict_mode=strict_mode,
            ),
        )

    # pylint: disable=too-many-arguments
    def get_integer_property(
        self,
        property_name: str,
        default_value: Optional[int] = None,
        valid_value_fn: Optional[Callable[[int], Any]] = None,
        is_required: bool = False,
        strict_mode: Optional[bool] = None,
    ) -> int:
        """
        Get an integer property from the configuration.
        """
        return cast(
            int,
            self.get_property(
                property_name,
                int,
                default_value=default_value,
                valid_value_fn=valid_value_fn,
                is_required=is_required,
                strict_mode=strict_mode,
            ),
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def get_string_property(
        self,
        property_name: str,
        default_value: Optional[str] = None,
        valid_value_fn: Optional[Callable[[str], Any]] = None,
        is_required: bool = False,
        strict_mode: Optional[bool] = None,
    ) -> str:
        """
        Get a string property from the configuration.
        """
        return cast(
            str,
            self.get_property(
                property_name,
                str,
                default_value=default_value,
                valid_value_fn=valid_value_fn,
                is_required=is_required,
                strict_mode=strict_mode,
            ),
        )

    # pylint: enable=too-many-arguments

    def property_names_under(self, key_name: str) -> List[str]:
        """
        List of each of the properties in the map under the specified key.
        """
        ApplicationProperties.verify_full_key_form(key_name)
        return [
            next_key_name
            for next_key_name in self.__flat_property_map
            if next_key_name.startswith(key_name)
        ]

    def __scan_map(self, config_map: Dict[Any, Any], current_prefix: str) -> None:
        for next_key, next_value in config_map.items():
            if not isinstance(next_key, str):
                raise ValueError(
                    "All keys in the main dictionary and nested dictionaries must be strings."
                )
            if (
                " " in next_key
                or "\t" in next_key
                or "\n" in next_key
                or ApplicationProperties.__assignment_operator in next_key
                or ApplicationProperties.__separator in next_key
            ):
                raise ValueError(
                    "Key strings cannot contain a whitespace character, "
                    + f"a '{ApplicationProperties.__assignment_operator}' character, or "
                    + f"a '{ApplicationProperties.__separator}' character."
                )

            if isinstance(next_value, dict):
                self.__scan_map(
                    next_value, f"{current_prefix}{next_key}{self.__separator}"
                )
            else:
                new_key = f"{current_prefix}{next_key}".lower()
                self.__flat_property_map[new_key] = copy.deepcopy(next_value)
                LOGGER.debug(
                    "Adding configuration '%s' : {%s}", new_key, str(next_value)
                )
