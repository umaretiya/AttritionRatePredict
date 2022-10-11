from attritionRate.constants import (
    CONFIG_FILE_PATH,
    MODEL_FILE_PATH,
    BASE_DIR,
    SCHEMA_FILE_PATH,
    CURRENT_TIMESTAMP,
)
from attritionRate.utils import read_yaml
from attritionRate.entity import (
    DataIngestionConfig,
    DataValidationConfig,
    ModelEvaluationConfig,
    ModelPusherConfig,
    ModelTrainingConfig,
    DataTransformationConfig,
    PipeLineConfig,
)

import os
from datetime import datetime


ROOT_DIR = BASE_DIR
DATA_INGESTION_DIR = "data_ingestion"
DATA_VALIDATION_DIR = "data_validation"
DATA_TRNASFORMATION_DIR = "data_transformation"
MODEL_TRAINING_DIR = "training"
MODEL_EVALUATING_DIR = "evaluation"
MODEL_PUSHER_DIR = "model_export"


class Configuration:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, current_timestamp=CURRENT_TIMESTAMP
    ):
        self.config_info = read_yaml(config_filepath)
        self.pipeline = self.get_training_pipeline()
        self.timestamp = current_timestamp

    def get_data_ingestion_config(self):
        artifacts = self.pipeline.artifact_dir
        data_ingestion_artifact = os.path.join(
            artifacts, DATA_INGESTION_DIR, self.timestamp
        )
        ingested_data = self.config_info.data_ingestion.destination_dir

        source_filename = self.config_info.data_ingestion.source_file
        source_filepath = os.path.join(BASE_DIR, source_filename)

        raw_dirfilepath = os.path.join(self.config_info.data_ingestion.raw_data_dir)
        raw_data = os.path.join(data_ingestion_artifact, raw_dirfilepath)

        destination_dir = os.path.join(data_ingestion_artifact, ingested_data)

        train_dir = os.path.join(
            destination_dir, self.config_info.data_ingestion.ingested_train_dir
        )
        test_dir = os.path.join(
            destination_dir, self.config_info.data_ingestion.ingested_test_dir
        )

        data_ingestion_config = DataIngestionConfig(
            source_file=source_filepath,
            dest_dir=raw_data,
            train_data=train_dir,
            test_data=test_dir,
        )
        return data_ingestion_config

    def get_data_validation_config(self):
        artifacts = self.pipeline.artifact_dir
        validation_data = self.config_info.data_validation_config
        # validation_dir = validation_data.data_validation_dir
        data_validation_artifact = os.path.join(
            artifacts, DATA_VALIDATION_DIR, self.timestamp
        )

        # data_validation_dir = os.path.join(artifacts,validation_dir,self.timestamp)

        schema_filepath = SCHEMA_FILE_PATH
        # report_filename': 'report.json', 'report_page_filename': 'report.html
        report_filename = validation_data.report_filename
        report_filepath = os.path.join(data_validation_artifact, report_filename)

        report_page_filename = validation_data.report_page_filename
        report_page_filepath = os.path.join(
            data_validation_artifact, report_page_filename
        )

        data_validation_config = DataValidationConfig(
            schema_filepath=schema_filepath,
            report_filepath=report_filepath,
            report_page_filepath=report_page_filepath,
        )
        return data_validation_config

    def get_data_transformation_config(self):
        artifacts = self.pipeline.artifact_dir
        data_transformation_artifact = os.path.join(
            artifacts, DATA_TRNASFORMATION_DIR, self.timestamp
        )

        transformd_data = self.config_info.data_transformation
        transformed_data_dir = transformd_data.transformed_data_dir
        # preprocessed_obj_dir = transformd_data.preprocessing_dir

        transformed_data_dirpath = os.path.join(
            data_transformation_artifact, transformed_data_dir
        )

        train_data_dir = transformd_data.transformed_train_dir
        train_data_path = os.path.join(transformed_data_dirpath, train_data_dir)

        test_data_dir = transformd_data.transformed_test_dir
        test_data_path = os.path.join(transformed_data_dirpath, test_data_dir)

        preprocessed_obj = transformd_data.preprocessing_dir

        preprocessed_obj_filename = transformd_data.preprocessed_object_file_name
        preprocessed_obj_filepath = os.path.join(
            data_transformation_artifact, preprocessed_obj, preprocessed_obj_filename
        )

        data_transformation_config = DataTransformationConfig(
            transformed_train_dir=train_data_path,
            transformed_test_dir=test_data_path,
            preprocessed_obj_path=preprocessed_obj_filepath,
        )
        return data_transformation_config

    def get_model_training_config(self):
        artifacts = self.pipeline.artifact_dir
        model_config_filepath = MODEL_FILE_PATH
        model_training_artifacts = os.path.join(
            artifacts, MODEL_TRAINING_DIR, self.timestamp
        )
        # 'model_training': {'trained_model_dir': 'trained_model', 'trained_model_name': 'model.pkl'}
        model_training_dir = self.config_info.model_training.trained_model_dir

        trained_model_file = os.path.join(
            model_training_dir, self.config_info.model_training.trained_model_name
        )

        model_trained_filepath = os.path.join(
            model_training_artifacts, trained_model_file
        )
        model_training_config = ModelTrainingConfig(
            model_config_filepath=model_config_filepath,
            model_train_filepath=model_trained_filepath,
        )
        return model_training_config

    def get_model_evaluation_config(self):
        artifacts = self.pipeline.artifact_dir
        model_evaluation_artifacts = os.path.join(
            artifacts, MODEL_EVALUATING_DIR, self.timestamp
        )

        model_evaluation = self.config_info.model_evaluating
        # 'model_evaluating': {'evaluated_model_dir': 'model_evaluation.yaml'}
        model_evaluating_filename = os.path.join(model_evaluation.evaluated_model_dir)

        model_evaluating_filepath = os.path.join(
            model_evaluation_artifacts, model_evaluating_filename
        )
        model_evaluation_config = ModelEvaluationConfig(
            model_evaluation_filepath=model_evaluating_filepath,
            time_stamp=self.timestamp,
        )
        return model_evaluation_config

    def get_model_pusher_config(self):
        # artifacts = self.pipeline.artifact_dir

        timestamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        model_pusher_artifacts = os.path.join(ROOT_DIR, MODEL_PUSHER_DIR, timestamp)

        model_pusher_config = ModelPusherConfig(
            export_dir_path=model_pusher_artifacts,
        )
        return model_pusher_config

    def get_training_pipeline(self):
        training_artifacts_config = self.config_info.artifacts_config
        project = training_artifacts_config.project
        pipeline_name = training_artifacts_config.pipeline
        artifacts_dir = training_artifacts_config.artifacts_dir

        artifact_dir = os.path.join(ROOT_DIR, project, pipeline_name, artifacts_dir)
        trainig_pipeline_config = PipeLineConfig(artifact_dir=artifact_dir)
        return trainig_pipeline_config
