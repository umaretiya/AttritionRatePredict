from pathlib import Path
from datetime import datetime
import os

# SCHEMA_FILE_PATH = Path("configs/schema.yaml")
# MODEL_FILE_PATH = Path("configs/model.yaml")
BASE_DIR = os.getcwd()

CONFIG_FILE_PATH = Path("configs/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")

SCHEMA_FILE_PATH = Path("configs/schema.yaml")
MODEL_FILE_PATH = Path("configs/model.yaml")


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


CURRENT_TIMESTAMP = get_current_time_stamp()
