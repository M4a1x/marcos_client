import logging
import sys
from importlib import resources as rsc
from pathlib import Path
from typing import Iterable

import platformdirs as pltfrm

try:
    import tomllib  # Python Version >= 3.11
except ModuleNotFoundError:
    import tomli as tomllib

logger = logging.getLogger(__name__)


def program_name() -> str:
    """Return the name of the program"""
    return __package__.split(".", maxsplit=1)[0]


def reload_config(additional_config_files: Iterable[Path] | None = None) -> dict:
    global config
    config = _load_config(additional_config_files)


def _load_config(additional_config_files: Iterable[Path] | None = None) -> dict:
    default_config_string = _load_default_config()
    _config = _parse_config_string(default_config_string)

    config_files = _find_config_files_in_default_directories()
    if additional_config_files:
        config_files.extend(additional_config_files)

    if not config_files:
        logger.error("Did not find any configuration file. Using defaults.")

    configs = _load_config_files(config_files)
    for cfg in configs:
        _config.update(cfg)

    return _config


def _save_default_config(config_path: Path) -> None:
    try:
        config_path.parent.mkdir(exist_ok=True, parents=True)
        with config_path.open(mode="w", encoding="utf-8") as cfg_file:
            cfg_file.write(_load_default_config())
        logger.info("Created default config file %s", str(config_path))
    except OSError as err:
        logger.warning(
            "Couldn't create default config file %s, due to error '%s'",
            str(config_path),
            err.strerror,
        )


def _load_default_config() -> str:
    """Load the default configuration"""
    return rsc.read_text("marcos_client", "local_config.toml.example")


def _find_config_files_in_default_directories() -> list[Path]:
    """Tries to find config files in the usual places, including next to the executable and lastly
    the current working directory that the command was executed in."""
    search_directories = [
        pltfrm.site_config_path(program_name()),
        pltfrm.user_config_path(program_name()),
        _next_to_executable_path(),
        Path().resolve(),  # cwd
    ]
    logger.info(
        "Looking for *.toml configuration files in the following directories: %s",
        [str(dir_) for dir_ in search_directories],
    )

    ini_config_files_nested = [list(dir_.glob("*.toml")) for dir_ in search_directories]
    config_files = [
        config_file
        for config_files in ini_config_files_nested
        for config_file in config_files
    ]

    logger.info(
        "Found the following configuration files: %s",
        [str(cfg) for cfg in config_files],
    )

    return config_files


def _load_config_files(config_files: "Iterable[Path]") -> list[dict]:
    """Load a list of config files"""
    configs = [_load_config_file(config_file) for config_file in config_files]
    logger.info(
        "Loaded the following configuration files in this order: %s",
        [
            str(filepath)
            for filepath, cfg in zip(config_files, configs, strict=True)
            if cfg
        ],
    )
    return configs


def _load_config_file(config_file: Path) -> dict:
    """Load the given config from file"""
    try:
        with config_file.open(mode="rb") as file:
            conf: dict = tomllib.load(file)
            return conf
    except tomllib.TOMLDecodeError as err:
        logger.warning(
            "Config file %s could not be loaded! Error was '%s'",
            str(config_file),
            err,
        )
        return {}


def _parse_config_string(config_string: str) -> dict:
    try:
        conf: dict = tomllib.loads(config_string)
        return conf
    except tomllib.TOMLDecodeError as err:
        logger.warning("Config string could not be loaded! Error was '%s'", err)
        return {}


def _next_to_executable_path() -> Path:
    """Get the full path to the folder that contains the currently executed module"""
    try:
        if _is_frozen():
            return Path(sys.executable).parent.resolve()
    except (AttributeError, NameError):
        return Path().resolve()  # cwd fallback
    # we are running in a normal Python environment
    return Path(__file__).parent.parent.resolve()


def _is_frozen() -> bool:
    """Check if we're running from inside a single executable/frozen installation"""
    return getattr(sys, "frozen", False)  # py2exe/cx_Freeze/PyInstaller


config = _load_config()
