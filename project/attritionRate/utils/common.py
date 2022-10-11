import os
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from typing import Any
import yaml
import json
import joblib
from attritionRate import logger
import pandas as pd
import dill


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    with open(path) as f:
        content = json.load(f)
    logger.info(f"json file loaded successfully form: {path}")
    return ConfigBox(content)


def save_bin(data: Any, path: Path):
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved successfuly {path}")


@ensure_annotations
def load_bin(path: str):
    data = joblib.load(path)
    logger.info(f"binary file loaded form: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~{size_in_kb} KB"


def load_data(file_path: Path, schema_filepath: Path):
    datatset_schema = read_yaml(schema_filepath)
    schema = datatset_schema.columns
    # print(schema)
    dataframe = pd.read_csv(file_path)
    # print(dataframe.columns)
    error_messgae = ""

    for column in dataframe.columns:
        if column in list(schema.keys()):
            dataframe[column].astype(schema[column])
        else:
            error_messgae = (
                f"{error_messgae} \nColumn: [{column}] is not in the schema."
            )
    if len(error_messgae) > 0:
        raise Exception(error_messgae)
    return dataframe


def save_object(file_path: str, obj):
    """
    file_path: str
    obj: Any sort of object
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as file_obj:
        dill.dump(obj, file_obj)


def load_object(file_path: str):
    """
    file_path: str
    """
    with open(file_path, "rb") as file_obj:
        return dill.load(file_obj)
