from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_dir: Path
    data_dir: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    prepro_obj_path: Path


@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
