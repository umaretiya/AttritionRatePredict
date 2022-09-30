from distutils.command.config import config
from attritionRate.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from attritionRate.utils import read_yaml, create_directories
from attritionRate.entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    TrainingConfig,
)
from pathlib import Path
import os


class ConfigurationManager:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_dir=config.source_dir,
            data_dir=config.data_dir,
        )
        return data_ingestion_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            prepro_obj_path=config.prepro_object_path,
        )
        return data_transformation_config

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        create_directories([training.root_dir])

        traing_config = TrainingConfig(
            root_dir=training.root_dir, trained_model_path=training.trained_model_path
        )
