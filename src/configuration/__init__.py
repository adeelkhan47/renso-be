import json
import logging
import os
from pathlib import Path


class Config:
    local_settings = None
    def __getattr__(cls, key):
        if key in cls.local_settings:
            return cls.local_settings[key]


configs = None
if not configs:
    configs = Config()
    project_root = str(Path(__file__).parent.parent.parent)
    try:
        with open(os.path.join(project_root, "etc", "configs.json"), "r") as file:
            data = json.load(file)
            if "ENVIRONMENT" not in data or data["ENVIRONMENT"] not in data:
                raise Exception("Unexpected settings file format, bad ENV")
            configs.local_settings = data[data["ENVIRONMENT"]]
    except FileNotFoundError:
        logging.error("Please add settings.local.json file in etc")
        raise
    except json.decoder.JSONDecodeError:
        logging.error("settings.local.json file not in a readable json format")
        raise
