import json
import os


class Config:
    def __init__(self, config_file="config.json"):
        self.config_path = os.path.abspath(config_file)
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, "r") as file:
            return json.load(file)

    def get_database_path(self, environment="development"):
        return self.config["database"].get(environment, {}).get("path")
