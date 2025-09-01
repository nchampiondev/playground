from blessed import Terminal
from menu import Menu
from http_client import HttpClient
from utils import Formatter
from scrollbox import ScrollableBox

class UIManager:
    def __init__(self, configs: list[dict]):
        self.term = Terminal()
        self.configs = configs
        self.http = HttpClient()
        self.formatter = Formatter(self.term)

    def run(self):
        with self.term.fullscreen():
            while True:
                main_menu = Menu(self.term, "API Manager", ["Manual Entry", "From Config", "Quit"])
                choice = main_menu.run()

                if choice is None or choice == 2:  # q pressed or Quit option
                    break
                elif choice == 0:
                    self._manual_entry()
                elif choice == 1 and self.configs:
                    self._from_config()

    def _manual_entry(self):
        print(self.term.clear)
        print(self.term.white("Manual Entry"))
        method = input("HTTP Method (only GET supported): ").upper()
        if method != "GET":
            print(self.term.bright_black("Only GET is supported."))
            input("\nPress Enter to return...")
            return
        url = input("URL: ")
        params = input("Query params (key=value&...): ")
        param_dict = dict(p.split("=") for p in params.split("&")) if params else {}
        result = self.http.get(url, param_dict)
        self._show_result(result)

    def _from_config(self):
        options = [ep["name"] for ep in self.configs]
        menu = Menu(self.term, "Choose Endpoint", options)
        idx = menu.run()
        if idx is None:  # user pressed q
            return
        selected = self.configs[idx]
        url = selected["url"].format(**selected.get("params", {}))
        result = self.http.get(url, selected.get("params"))
        self._show_result(result)

    def _show_result(self, result: dict):
        formatted = self.formatter.pretty_json(result).splitlines()
        scrollbox = ScrollableBox(self.term, formatted)
        scrollbox.run()
