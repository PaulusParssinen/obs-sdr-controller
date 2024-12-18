from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Placeholder

from ..widgets.console import Console
from ..widgets.header import Header


class Main(Screen[None]):
  """The main screen of the application."""

  TITLE = "Main"

  def __init__(self) -> None:
    super().__init__()

  def compose(self) -> ComposeResult:
    yield Header(name="OBS SDR Controller")
    with Vertical():
      yield Placeholder(id="main")
      yield Console()