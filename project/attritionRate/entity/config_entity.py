from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    dataset_url: str
    dataset_dir: Path
    ingested_dir: Path
    raw_data_dir: Path
    dataset: str


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    prepro_obj_path: Path
    clean_data_dir: Path
    serialized_obj_dir: Path
    marketing_compaign_csv_file: str


@dataclass(frozen=True)
class DataTransformationConfig:
    transformed_data_dir: Path


@dataclass(frozen=True)
class TrainingConfig:
    trained_model_dir: Path
    trained_model_name: str
