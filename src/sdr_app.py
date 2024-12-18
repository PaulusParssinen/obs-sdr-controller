from textual.app import App

from .tui.screens.main import Main

# logging.basicConfig(
#     level=logging.DEBUG, format="%(message)s", datefmt="[%X]",
#     handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[
#                           marshmallow, dataclasses_json, obsws_python, asyncio])]
# )

class SdrControlApp(App):
  """The main application class for the SDR controller."""

  ENABLE_COMMAND_PALETTE = False

  CSS_PATH = "tui/app.tcss"
  
  def on_mount(self) -> None:
    self.push_screen(Main())