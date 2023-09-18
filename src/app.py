from typing import ClassVar

from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.screen import Screen
from textual.widgets import Footer, Header, LoadingIndicator, Pretty

from client import Client


class LoadingScreen(Screen):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator()


class NubankApp(App[None]):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("q", "quit", "Quit app", show=True),
    ]
    CSS_PATH: ClassVar[str] = "main.css"
    SCREENS = {"loading_screen": LoadingScreen()}

    def compose(self) -> ComposeResult:
        self.client = Client()
        self.client.load_bills()
        yield Header(show_clock=True)

        # id = self.client.bills[8].id
        # if id:
        #     b = self.client.get_bill_details(id)
        #     l = Pretty(b)
        #     yield l

        yield Pretty(self.client.bills[7])
        yield Footer()


if __name__ == "__main__":
    app = NubankApp()
    app.run()
