import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Optional

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

PROJECT_NAME = "md_dead_link_check"

DEFAULT_CATCH_RESPONSE_CODES = [
    404,  # Not found
    410,  # Gone
    500,  # Internal Server Error (for cannot connect to host under proxy)
]


@dataclass
class Config:
    timeout: int = 5
    catch_response_codes: list[int] = field(default_factory=lambda: DEFAULT_CATCH_RESPONSE_CODES)
    exclude_links: list[str] = field(default_factory=lambda: [])
    exclude_files: list[str] = field(default_factory=lambda: [])
    force_get_requests_for_links: list[str] = field(default_factory=lambda: [])
    check_web_links: bool = True
    validate_ssl: bool = True
    throttle_groups: int = 100
    throttle_delay: int = 20
    throttle_max_delay: int = 100


def get_config(root_dir: Path, config_path: Optional[Path]) -> Config:
    if not config_path:
        config_path = root_dir / "pyproject.toml"
    config = Config()

    if config_path.is_file():
        with open(config_path, "rb") as handle:
            pyproject_toml = tomllib.load(handle)
        toml_config: dict[str, Any] = pyproject_toml.get("tool", {}).get(PROJECT_NAME, {})

        for key, value in toml_config.items():
            if hasattr(config, key):
                setattr(config, key, value)
            else:
                msg = (
                    f"Unexpected config key `{key}` in {config_path.name}. "
                    f"Available keys: [{', '.join(config.__annotations__)}]"
                )
                raise ValueError(msg)
    if not isinstance(config.timeout, int) or config.timeout < 1:
        msg = "`timeout` must be an integer greater than or equal to 1."
        raise ValueError(msg)
    if not isinstance(config.throttle_groups, int) or config.throttle_groups < 1:
        msg = "`throttle_groups` must be an integer greater than or equal to 1."
        raise ValueError(msg)
    if not isinstance(config.throttle_delay, int) or config.throttle_delay < 0:
        msg = "`throttle_delay` must be a non-negative float or integer."
        raise ValueError(msg)
    if not isinstance(config.throttle_max_delay, int) or config.throttle_max_delay < 0:
        msg = "`throttle_max_delay` must be a non-negative integer."
        raise ValueError(msg)
    return config
