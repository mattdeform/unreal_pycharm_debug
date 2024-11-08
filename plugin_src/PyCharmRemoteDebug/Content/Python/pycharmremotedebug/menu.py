import unreal

from .actions import (
    PyCharmRemoteDebugConnect,
    PyCharmRemoteDebugDisconnect,
    PyCharmRemoteDebugConfig,
)


LEVEL_EDITOR_MENU = "LevelEditor.MainMenu"


def install() -> None:
    """Install the PyCharm remote debugger menu items into the level editor"""
    tool_menus = unreal.ToolMenus.get()
    tool_bar = tool_menus.find_menu(LEVEL_EDITOR_MENU)

    start_action = PyCharmRemoteDebugConnect()
    stop_action = PyCharmRemoteDebugDisconnect()
    config_action = PyCharmRemoteDebugConfig()

    dbg_menu = tool_bar.add_sub_menu(
        "dbg_menu", "Python", "PyCharmRemoteDebug", "PyCharm"
    )

    for action in [start_action, stop_action, config_action]:
        menu_entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.MENU_ENTRY)
        menu_entry.script_object = action
        dbg_menu.add_menu_entry("Items", menu_entry)

    tool_menus.refresh_all_widgets()
