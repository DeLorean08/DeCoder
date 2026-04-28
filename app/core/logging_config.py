import logging
import logging.config
import os
from pathlib import Path

import yaml

def setup_logging(yaml_path: str = "app/core/settings_logging.yaml"):
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            yaml_config = yaml.safe_load(f.read())

        Path("logs").mkdir(exist_ok=True)
        
        logging.config.dictConfig(yaml_config)
    else:
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Logging configuration file {yaml_path} not found. Using basic config.")



    
