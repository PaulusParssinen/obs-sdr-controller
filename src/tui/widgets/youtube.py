from textual.containers import Container
from textual.widgets import Static, Button, Select
from textual.app import ComposeResult, App
from textual.worker import Worker, WorkerState
from typing import List
import threading

class AuthScreen(Static):
  def compose(self) -> ComposeResult:
    yield Button("Authenticate", id="auth_button")

  def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "auth_button":
      # Handle OAuth authentication logic here
      self.parent.push_screen(BroadcastSelectScreen(broadcasts=["Broadcast 1", "Broadcast 2"]))

class BroadcastSelectScreen(Static):
  def __init__(self, broadcasts: List[str]):
    super().__init__()
    self.broadcasts = broadcasts

  def compose(self) -> ComposeResult:
    yield Select(options=self.broadcasts, id="broadcast_select")
    yield Button("Start Logging", id="start_logging_button")

  def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "start_logging_button":
      selected_broadcast = self.query_one("#broadcast_select").value
      # Start logging live chat in a separate thread
      self.start_logging(selected_broadcast)

  def start_logging(self, broadcast: str) -> None:
    def log_chat():
      # Logic to log live chat in real-time
      pass

    threading.Thread(target=log_chat, daemon=True).start()