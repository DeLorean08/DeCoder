import logging
import os
from pathlib import Path

import yaml

def setup_logging(yaml_path: str = "app/core/logging.yaml"):
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f.read())

        Path("logs").mkdir(exist_ok=True)
        
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Logging configuration file {yaml_path} not found. Using basic config.")



    
