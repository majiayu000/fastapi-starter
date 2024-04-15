import configparser


class Config:
    def __init__(self, config_file: str = "config.ini"):
        self.cfg = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        self.cfg.read(self.config_file)
        self.env = self.cfg["ENV"]["ENV"]

    def get_config(self, key):
        return self.cfg[self.env][key]
