from typing import ClassVar

from pynubank import Nubank
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.screen import Screen
from textual.widgets import Footer, Header, LoadingIndicator, Pretty

from config import Config
from models.card_statement import CardStatement


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
        self._setup()
        s = self.nu.get_card_statements()[0]
        s = CardStatement(**s)

        l = Pretty(s)
        yield Header(show_clock=True)
        yield l
        yield Footer()

    def _setup(self):
        self.nu = Nubank()
        settings = Config()
        self.nu.authenticate_with_cert(settings.cpf, settings.password, "cert.p12")


if __name__ == "__main__":
    app = NubankApp()
    app.run()
