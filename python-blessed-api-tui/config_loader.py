import yaml

class ConfigLoader:
    def __init__(self, path: str):
        self.path = path

    def load(self):
        try:
            with open(self.path, "r") as f:
                data = yaml.safe_load(f)
            return [
                ep for ep in data.get("endpoints", [])
                if ep.get("method", "GET").upper() == "GET"
            ]
        except FileNotFoundError:
            return []
