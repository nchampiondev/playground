# scrollbox.py
from blessed import Terminal

class ScrollableBox:
    def __init__(self, term: Terminal, content_lines: list[str]):
        self.term = term
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

                # Fill empty space if not enough lines
                for _ in range(self.height - len(visible)):
                    print("│" + " " * self.width + "│")

                # Bottom border
                print("└" + "─" * self.width + "┘")

                print(self.term.bright_black("\n↑/↓ scroll, q to quit"))

                key = self.term.inkey()
                if key.name == "KEY_UP" and self.scroll > 0:
                    self.scroll -= 1
                elif key.name == "KEY_DOWN" and self.scroll < len(self.content_lines) - self.height:
                    self.scroll += 1
                elif key.lower() in ("q", "KEY_ESCAPE"):
                    break
