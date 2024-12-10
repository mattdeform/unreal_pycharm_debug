import unreal


ACTION_NAME = "stop_debugger"
ACTION_LABEL = "Disconnect"
ICON_STYLE = "EditorStyle"
ICON_NAME = "Sequencer.IconKeyAuto"


@unreal.uclass()
class PyCharmDebugDisconnect(unreal.ToolMenuEntryScript):
    """Menu action to disconnect from a PyCharm debugger"""

    @unreal.ufunction(override=True)
    def execute(
        self, context: unreal.ToolMenuContext  # pylint: disable=(unused-argument)
    ) -> None:
        """Disconnect from the PyCharm debugger

        Args:
            context (unreal.ToolMenuContext): ToolMenuContext context object
        """
        try:
            import pydevd
        except ImportError:
            return

        pydevd.stoptrace()
        unreal.log("Disconnected from PyCharm debugger")

    def __init__(self) -> None:
        super().__init__()
        self.data.name = ACTION_NAME
        self.data.label = ACTION_LABEL
        self.data.icon = unreal.ScriptSlateIcon(ICON_STYLE, ICON_NAME)
