from blessed import Terminal

class BaseScreen:
    def __init__(self, term: Terminal):
        self.term = term

    def draw_footer(self):
        """Always draw the navigation label at the bottom."""
        with self.term.location(0, self.term.height - 1):
            print(self.term.bright_black("↑/↓ scroll, q to quit"))
