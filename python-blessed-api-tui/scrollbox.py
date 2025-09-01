from base_screen import BaseScreen

class ScrollableBox(BaseScreen):
    def __init__(self, term, content_lines: list[str]):
        super().__init__(term)
        self.content_lines = content_lines
        self.scroll = 0
        self.height = term.height // 2
        self.width = term.width - 4

    def run(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear)

                # Top border
                print("┌" + "─" * self.width + "┐")

                # Visible slice
                visible = self.content_lines[self.scroll:self.scroll + self.height]
                for line in visible:
                    print("│" + line[:self.width].ljust(self.width) + "│")

                # Fill empty space
                for _ in range(self.height - len(visible)):
                    print("│" + " " * self.width + "│")

                # Bottom border
                print("└" + "─" * self.width + "┘")

                self.draw_footer()  # <-- common footer

                key = self.term.inkey()
                if key.name == "KEY_UP" and self.scroll > 0:
                    self.scroll -= 1
                elif key.name == "KEY_DOWN" and self.scroll < len(self.content_lines) - self.height:
                    self.scroll += 1
                elif key.lower() == "q":
                    break
