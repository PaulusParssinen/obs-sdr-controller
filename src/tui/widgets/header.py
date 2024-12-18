from datetime import datetime
from rich.text import Text
from textual.app import RenderResult
from textual.dom import NoScreen
from textual.events import Mount
from textual.reactive import Reactive
from textual.widget import Widget

class HeaderClock(Widget):
    """Display a clock on the right of the header."""

    DEFAULT_CSS = """
    HeaderClock {
        dock: right;
        width: 10;
        padding: 0 1;

        background: $foreground-darken-1 5%;
        color: $text;
        text-opacity: 85%;
        content-align: center middle;
    }
    """

    def _on_mount(self, _: Mount) -> None:
        self.set_interval(1, callback=self.refresh, name="header clock refresh")

    def render(self) -> RenderResult:
        return Text(datetime.now().time().strftime("%X") + "Z")

class HeaderTitle(Widget):
    """Display the title / subtitle in the header."""

    DEFAULT_CSS = """
    HeaderTitle {
        content-align: center middle;
        width: 100%;
    }
    """

    text: Reactive[str] = Reactive("")
    """The main title text."""

    sub_text = Reactive("")
    """The sub-title text."""

    def render(self) -> RenderResult:
        text = Text(self.text, no_wrap=True, overflow="ellipsis")
        if self.sub_text:
            text.append(" — ")
            text.append(self.sub_text, "dim")
        return text

class Header(Widget):
    """A header widget with icon and clock."""

    DEFAULT_CSS = """
    Header {
        dock: top;
        width: 100%;
        background: $foreground 5%;
        color: $text;
        height: 1;
    }
    """

    DEFAULT_CLASSES = ""

    def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)

    def compose(self):
        self._title = HeaderTitle()

        yield self._title
        yield HeaderClock()

    @property
    def screen_title(self) -> str:
        """The title that this header will display."""
        screen_title = self.screen.title
        title = screen_title if screen_title is not None else self.app.title
        return title

    @property
    def screen_sub_title(self) -> str:
        """The sub-title that this header will display."""
        screen_sub_title = self.screen.sub_title
        sub_title = (
            screen_sub_title if screen_sub_title is not None else self.app.sub_title
        )
        return sub_title

    def _on_mount(self, _: Mount) -> None:
        async def set_title() -> None:
            try:
                self._title.text = self.screen_title
            except NoScreen:
                pass

        async def set_sub_title() -> None:
            try:
                self._title.sub_text = self.screen_sub_title
            except NoScreen:
                pass

        self.watch(self.app, "title", set_title)
        self.watch(self.app, "sub_title", set_sub_title)
        self.watch(self.screen, "title", set_title)
        self.watch(self.screen, "sub_title", set_sub_title)