from pathlib import Path
import os
import json
from typing import Union

from unreal import (
    PluginBlueprintLibrary,
    log_error,
)


DEFAULT_PORT_NUMBER = 5678
MIN_PORT_NUMBER = 0
MAX_PORT_NUMBER = 65535  # unsigned 16-bit integer range for port numbers
PLUGIN_NAME = "pycharm_remote_debug"
RELATIVE_CONFIG_PATH = "Config/tool_config.json"


def get_plugin_config(create_on_fail=False) -> Union[Path, None]:
    """Get the path to the tool config file

    Args:
        create_on_fail (bool): If the lookup fails, create the config file,
        defaults to False

    Returns:
        str: The path to the tool config file
    """
    plugin_root = PluginBlueprintLibrary.get_plugin_base_dir(PLUGIN_NAME)
    if plugin_root is None:
        log_error("Failed to resolve plugin root directory")
        return None

    resolved_plugin_config = Path(plugin_root).joinpath(RELATIVE_CONFIG_PATH)

    if resolved_plugin_config.exists() is False:
        if create_on_fail:
            resolved_plugin_config.touch()
        else:
            log_error("Failed to resolve plugin config")

    return resolved_plugin_config


def get_debug_port() -> Union[int, None]:
    """Get the port number from the config file

    Returns:
        int: The port number
    """
    plugin_config = get_plugin_config()

    if plugin_config is None:
        return DEFAULT_PORT_NUMBER

    with open(plugin_config.as_posix(), "r", encoding="utf-8") as file:
        data = json.load(file)

    port_number = data.get("port_number", DEFAULT_PORT_NUMBER)
    if port_number is None:
        # port number key is present but value is None, default to 5678
        port_number = DEFAULT_PORT_NUMBER

    return port_number


def set_debug_port(port: int) -> bool:
    """Set the port number in the config
    Args:
        port (int): The port number to set
    """
    if isinstance(port, int) is False:
        log_error("Port must be an integer")
        return False

    if port < MIN_PORT_NUMBER or port > MAX_PORT_NUMBER:
        log_error("Port must be between 0 and 65535")
        return False

    plugin_config = get_plugin_config(create_on_fail=True)

    if plugin_config is None:
        return False  # failed to find or create plugin config

    with open(plugin_config.as_posix(), "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    data["port_number"] = port

    with open(plugin_config.as_posix(), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return True


def find_system_dbg_egg() -> Union[str, None]:
    """Attempt to find the debug egg from the system PyCharm installation

    Returns:
        Union[str, None]: Path to the PyCharm installation debug egg or None
    """
    pycharm_bin_dir = os.environ.get("PyCharm")
    if pycharm_bin_dir is None:
        log_error("PyCharm installation not found")
        return None

    pycharm_dir_path: Path = Path(pycharm_bin_dir.split(";")[0])

    if pycharm_dir_path.is_dir() is False:
        log_error("PyCharm bin path not found")
        return None

    egg_path: Path = pycharm_dir_path.parent.joinpath("debug-eggs/pydevd-pycharm.egg")

    if egg_path.is_file() is False:
        log_error("System debug egg not found")
        return None

    return egg_path.as_posix()


def get_debug_egg() -> Union[str, None]:
    """Get the debug egg location from the config file, if that fails,
    attempt to find the system PyCharm installation debug egg.

    Returns:
        Union[str, None]: Path to the debug egg or None
    """
    plugin_config = get_plugin_config()

    data = {}
    if plugin_config:
        with open(plugin_config.as_posix(), "r", encoding="utf-8") as file:
            data = json.load(file)

    egg_loc = data.get("debug_egg")

    if egg_loc is None or Path(egg_loc).is_file() is False:
        egg_loc = find_system_dbg_egg()

        if egg_loc is None or Path(egg_loc).is_file() is False:
            log_error("Failed to resolve a debug egg")
            return None

        log_error("No saved debug egg found in config, using system default")

    return egg_loc


def set_debug_egg(location: str) -> bool:
    """Set the debug egg location in the config file

    Args:
        location (str): The location of the debug egg

    Returns:
        bool: True if the operation was successful
    """
    plugin_config = get_plugin_config(create_on_fail=True)

    if plugin_config is None:
        return False  # failed to find or create plugin config

    with open(plugin_config.as_posix(), "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    egg_path = Path(location)

    if egg_path.is_file() is False or egg_path.name != "pydevd-pycharm.egg":
        log_error("Invalid egg file")
        return False

    data["debug_egg"] = location

    with open(plugin_config.as_posix(), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return True
