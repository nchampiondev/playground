import json
from blessed import Terminal

class Formatter:
    def __init__(self, term: Terminal):
        self.term = term

    def pretty_json(self, data: dict) -> str:
        raw = json.dumps(data, indent=2)
        lines = []
        for line in raw.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                lines.append(self.term.gray(key + ":") + self.term.white(value))
            else:
                lines.append(self.term.white(line))
        return "\n".join(lines)
