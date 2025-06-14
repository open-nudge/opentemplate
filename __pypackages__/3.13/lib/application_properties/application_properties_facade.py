"""
Module to provide for a facade in front of an ApplicationProperties instance that
only exposes part of the properties tree.
"""

import logging
from typing import Any, Callable, List, Optional

from application_properties.application_properties import ApplicationProperties

LOGGER = logging.getLogger(__name__)


class ApplicationPropertiesFacade:
    """
    Class to provide for a facade in front of an ApplicationProperties instance that
    only exposes part of the properties tree.
    """

    def __init__(
        self, base_properties: ApplicationProperties, property_prefix: str
    ) -> None:
        """
        Initializes an new instance of the ApplicationPropertiesFacade class.
        """
        if not isinstance(base_properties, ApplicationProperties):
            raise ValueError(
                "The base_properties of the facade must be an ApplicationProperties instance."
            )
        self.__base_properties = base_properties

        if not isinstance(property_prefix, str):
            raise ValueError("The property_prefix argument must be a string.")
        if not property_prefix.endswith(base_properties.separator):
            raise ValueError(
                f"The property_prefix argument must end with the separator character '{base_properties.separator}'."
            )
        self.__property_prefix = property_prefix

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

        return self.__base_properties.get_property(
            f"{self.__property_prefix}{property_name}",
            property_type,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    def get_boolean_property(
        self,
        property_name: str,
        default_value: Optional[bool] = None,
        is_required: bool = False,
    ) -> bool:
        """
        Get a boolean property from the configuration.
        """
        return self.__base_properties.get_boolean_property(
            f"{self.__property_prefix}{property_name}",
            default_value=default_value,
            is_required=is_required,
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
        return self.__base_properties.get_integer_property(
            f"{self.__property_prefix}{property_name}",
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
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
        return self.__base_properties.get_string_property(
            f"{self.__property_prefix}{property_name}",
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    @property
    def property_names(self) -> List[str]:
        """
        List of each of the properties in the map.
        """
        return [
            next_property_name[len(self.__property_prefix) :]
            for next_property_name in self.__base_properties.property_names
            if next_property_name.startswith(self.__property_prefix)
        ]

    def property_names_under(self, key_name: str) -> List[str]:
        """
        List of each of the properties in the map under the specified key.
        """
        ApplicationProperties.verify_full_key_form(key_name)
        return [
            next_key_name
            for next_key_name in self.property_names
            if next_key_name.startswith(key_name)
        ]
