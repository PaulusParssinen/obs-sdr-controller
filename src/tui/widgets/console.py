import asyncio
import logging
import rich
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Input, RichLog

#class ConsoleLog(RichLog):

class RichLogHandler(logging.Handler):
    def __init__(self, rich_log_widget: RichLog, level=logging.NOTSET):
        super().__init__(level)
        self.rich_log_widget = rich_log_widget

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

            self.rich_log_widget.write(log_entry)

        except Exception:
            self.handleError(record)

class Console(Widget):
    """A console widget for executing commands and viewing application log."""
    
    def compose(self) -> ComposeResult:
        self._rich_log = RichLog(id="console-log", markup=True)
        rich_handler = RichLogHandler(self._rich_log)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        rich_handler.setFormatter(formatter)

        self._log = logging.getLogger("console")
        self._log.setLevel(logging.DEBUG)
        self._log.addHandler(rich_handler)

        with Vertical():
          with Horizontal(id="run-command-bar"):
            yield Input("Run command: ", id="run-command")
            yield Button("Run", id="run-button")
          yield self._rich_log

    def on_mount(self) -> None:
        asyncio.create_task(self.delayed_test_log())
    
    async def delayed_test_log(self):
        for i in range(200):
            await asyncio.sleep(0.1)
            self._log.info(f"Test log message {i}")
            if i % 2 == 0:
                self._log.debug(f"Test debug message {i}")
            if i % 3 == 0:
                self._log.warning(f"Test warning message {i}")