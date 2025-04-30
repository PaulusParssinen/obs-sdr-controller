import asyncio
import logging
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Input

from youtube import YouTubeAPI

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

  @on(Button.Pressed, "#connect-button")
  def connect(self, message: Button.Pressed):
    message.stop()
    self.app.log.info("Connecting to OBS")

class YoutubeOptions(Container):
  """A container for the YouTube options."""

  BORDER_TITLE = "YouTube"

  def __init__(self, youtube: YouTubeAPI) -> None:
    super().__init__()

    self._youtube = youtube

  def compose(self) -> ComposeResult:
    yield Input(placeholder="YouTube API Key", id="youtube-api-key")
    yield Button("Connect", id="connect-button")

  @on(Button.Pressed, "#connect-button")
  def connect(self, message: Button.Pressed):
    message.stop()
    self.app.log.info("Connecting to YouTube")
    self._youtube

class Main(Screen[None]):
  """The main screen of the application."""

  TITLE = "Main"

  def __init__(self) -> None:
    super().__init__()

    self._log = logging.getLogger("app")
    self._log.setLevel(logging.DEBUG)

  def compose(self) -> ComposeResult:
    yield Header(name="OBS SDR Controller")
    with Vertical():
      with Vertical(id="main"):
        with HorizontalGroup():
          yield OBSOptions()
          yield YoutubeOptions()
      yield Console()
  
  def on_mount(self) -> None:
        asyncio.create_task(self.delayed_test_log())
    
  async def delayed_test_log(self):
      for i in range(50):
          await asyncio.sleep(0.5)
          self._log.warning(f"from main: test log message {i}")