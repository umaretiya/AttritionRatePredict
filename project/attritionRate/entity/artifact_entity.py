from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionArtifact:
    train_data: Path
    test_data: Path


@dataclass(frozen=True)
class DataValidationArtifact:
    report_file: Path
    report_page_file: Path
    schema_filepath: Path
    is_validated: bool


@dataclass(frozen=True)
class DataTransformationArtifact:
    train_data: Path
    test_data: Path
    preprocessed_obj_path: Path


@dataclass(frozen=True)
class ModelTrainingArtifact:
    trained_model_path: Path
    train_accuracy: float
    test_acuuracy: float
    model_accuracy: float


@dataclass(frozen=True)
class MetricInfoArtifact:
    model_name: str
    model_object: str
    train_accuracy: float
    test_accuracy: float
    train_f1_score: float
    test_f1_score: float
    model_accuracy: float


@dataclass
class GridSearchBestModel:
    model_serial_number: int
    model: object
    best_model: object
    best_parameters: dict
    best_score: float
