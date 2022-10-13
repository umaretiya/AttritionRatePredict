from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipeLineConfig:
    artifact_dir: Path


@dataclass(frozen=True)
class DataIngestionConfig:
    source_file: str
    dest_dir: Path
    train_data: Path
    test_data: Path


@dataclass(frozen=True)
class DataValidationConfig:
    schema_filepath: Path
    report_filepath: Path
    report_page_filepath: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    transformed_train_dir: Path
    transformed_test_dir: Path
    preprocessed_obj_path: Path


@dataclass(frozen=True)
class ModelTrainingConfig:
    model_config_filepath: Path
    model_train_filepath: object


@dataclass(frozen=True)
class ModelEvaluationConfig:
    model_evaluation_filepath: Path
    time_stamp: str
    export_dir_path: Path


@dataclass(frozen=True)
class InitializedModel:
    model_serial_number: int
    model: object
    param_grid_search: dict
    model_name: str
