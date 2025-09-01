from blessed import Terminal
from base_screen import BaseScreen

class Menu(BaseScreen):
    def __init__(self, term: Terminal, title: str, options: list[str]):
        super().__init__(term)
        self.title = title
        self.options = options
        self.index = 0

    def run(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear)
                print(self.term.white(self.title))
                for i, opt in enumerate(self.options):
                    if i == self.index:
                        print(self.term.reverse(opt))  # selected
                    else:
                        print(self.term.bright_black(opt))

                self.draw_footer()  # <-- common footer

                key = self.term.inkey()
                if key.name == "KEY_UP":
                    self.index = (self.index - 1) % len(self.options)
                elif key.name == "KEY_DOWN":
                    self.index = (self.index + 1) % len(self.options)
                elif key.name in ("KEY_ENTER", "ENTER"):
                    return self.index
                elif key.lower() == "q":
                    return None
