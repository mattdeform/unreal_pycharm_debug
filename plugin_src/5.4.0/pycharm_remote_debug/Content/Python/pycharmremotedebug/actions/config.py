import unreal


ACTION_NAME = "config_debugger"
ACTION_LABEL = "Configure"
ICON_STYLE = "EditorStyle"
ICON_NAME = "AutomationTools.MenuIcon"
CONFIG_WIDGET_PATH = "/pycharm_remote_debug/Blueprints/Widgets/EUW_PCRD_CONFIG"


@unreal.uclass()
class PyCharmRemoteDebugConfig(unreal.ToolMenuEntryScript):
    """Menu action to configure the PyCharm remote debugger"""

    def __init__(self) -> None:
        super().__init__()
        self.data.name = ACTION_NAME
        self.data.label = ACTION_LABEL
        self.data.icon = unreal.ScriptSlateIcon(ICON_STYLE, ICON_NAME)

    @unreal.ufunction(override=True)
    def execute(
        self, context: unreal.ToolMenuContext  # pylint: disable=(unused-argument)
    ) -> None:
        """Open PyCharm remote debugger configuration widget

        Args:
            context (unreal.ToolMenuContext): ToolMenuContext context object
        """
        asset = unreal.EditorAssetLibrary.load_asset(CONFIG_WIDGET_PATH)
        euss = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
        bp = euss.find_utility_widget_from_blueprint(asset)

        if bp:  # don't spawn a second widget
            return

        euss.spawn_and_register_tab(asset)
