from ui import UIManager
from config_loader import ConfigLoader

def main():
    configs = ConfigLoader("config.yaml").load()
    ui = UIManager(configs)
    ui.run()

if __name__ == "__main__":
    main()
