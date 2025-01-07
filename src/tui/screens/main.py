from textual.app import ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Input, Placeholder

from ..widgets.console import Console
from ..widgets.header import Header

class OBSOptions(Container):
  """A container for the OBS options."""

  BORDER_TITLE = "OBS"

  def compose(self) -> ComposeResult:
    yield Input(placeholder="OBS Host", id="obs-host")
    yield Input(placeholder="OBS Port", id="obs-port")
    yield Input(placeholder="OBS Password", id="obs-password")
    yield Button("Connect", id="connect-button")

class YoutubeOptions(Container):
  """A container for the YouTube options."""

  BORDER_TITLE = "YouTube"

  def compose(self) -> ComposeResult:
    yield Input(placeholder="YouTube API Key", id="youtube-api-key")
    yield Button("Connect", id="connect-button")

class Main(Screen[None]):
  """The main screen of the application."""

  TITLE = "Main"

  # def __init__(self) -> None:
  #   super().__init__()

  def compose(self) -> ComposeResult:
    yield Header(name="OBS SDR Controller")
    with Vertical():
      with Vertical(id="main"):
        with HorizontalGroup():
          yield OBSOptions()
          yield YoutubeOptions()
      yield Console()