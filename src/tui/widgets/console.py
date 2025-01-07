import asyncio
import logging
import rich
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup
from textual.widget import Widget
from textual.widgets import Button, Input, Label, RichLog, Rule

class RichLogHandler(logging.Handler):
    def __init__(self, log_widget: RichLog, level=logging.NOTSET):
        super().__init__(level)
        self._log_widget = log_widget

    def emit(self, record):
        try:
            # Format the log message
            log_entry = self.format(record)

            # Add log level specific styling
            if record.levelno == logging.DEBUG:
                log_entry = f"[dim]{log_entry}[/dim]"
            elif record.levelno == logging.INFO:
                log_entry = f"[green]{log_entry}[/green]"
            elif record.levelno == logging.WARNING:
                log_entry = f"[yellow]{log_entry}[/yellow]"
            elif record.levelno == logging.ERROR:
                log_entry = f"[bold red]{log_entry}[/bold red]"
            elif record.levelno == logging.CRITICAL:
                log_entry = f"[bold white on red]{log_entry}[/bold white on red]"

            self._log_widget.write(log_entry)

        except Exception:
            self.handleError(record)

class Console(Container):
    """A console widget for executing commands and viewing application log."""
    
    BORDER_TITLE = "Console"

    def compose(self) -> ComposeResult:
        self._rich_log = RichLog(id="console-log", markup=True)
        rich_handler = RichLogHandler(self._rich_log)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        rich_handler.setFormatter(formatter)

        self._log = logging.getLogger("console")
        self._log.setLevel(logging.DEBUG)
        self._log.addHandler(rich_handler)

        with VerticalGroup():
          with HorizontalGroup(id="command-bar"):
            yield Label("Command:")
            yield Input(placeholder="!stats", id="command")
            yield Button("Execute", id="execute-button")
          yield Rule()
          yield self._rich_log

    def on_mount(self) -> None:
        asyncio.create_task(self.delayed_test_log())
    
    async def delayed_test_log(self):
        for i in range(50):
            await asyncio.sleep(0.1)
            self._log.info(f"Test log message {i}")
    
    @on(Button.Pressed, "#execute-button")
    def on_execute_button(self) -> None:
        input = self.cmd_input
        command = input.value

        self._log.info(f"Executing command: {command}")
        input.clear()
    
    @on(Input.Submitted, "#command")
    def on_submit_command(self, event: Input.Submitted):
        self._log.info(f"Executing command: {event.value}")
        event.input.clear()

    @property
    def cmd_input(self) -> Input:
        return self.query_one("#command", Input)