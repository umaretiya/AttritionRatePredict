from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import os
import json

from attritionRate.constants import (
    SCHEMA_FILE_PATH,
)
from attritionRate.utils import read_yaml, create_directories
from attritionRate.entity import DataValidationConfig
from attritionRate.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
import pandas as pd


class DataValidation:
    def __init__(
        self,
        data_ingestion: DataIngestionArtifact,
        data_validation: DataValidationConfig,
    ):
        self.data_ingestion_artifacts = data_ingestion
        self.data_validation_config = data_validation

    def get_train_test_df(self):
        train_df = pd.read_csv(self.data_ingestion_artifacts.train_data)
        test_df = pd.read_csv(self.data_ingestion_artifacts.test_data)
        return train_df, test_df

    def is_train_test_df_available(self):
        is_train_df_path = os.path.exists(self.data_ingestion_artifacts.train_data)
        is_test_df_path = os.path.exists(self.data_ingestion_artifacts.test_data)

        is_avialable = is_train_df_path and is_test_df_path

        if not is_avialable:
            train = self.data_ingestion_artifacts.train_data
            test = self.data_ingestion_artifacts.test_data
            messages = f"{train} and {test} not available"
            raise Exception(messages)

        return is_avialable

    def vlaidation_datasets_schema(self):
        is_validated_schema = False
        schema = read_yaml(SCHEMA_FILE_PATH)
        schema_col = schema.columns

        df = pd.read_csv(self.data_ingestion_artifacts.train_data)

        for i in schema_col:
            if schema_col[i] == df[i].dtype:
                is_validated_schema = True

        return is_validated_schema

    def get_and_save_data_drift_report(self):
        profile = Profile(sections=[DataDriftProfileSection()])

        train_df, test_df = self.get_train_test_df()
        profile.calculate(train_df, test_df)
        report = json.loads(profile.json())

        report_filepath = self.data_validation_config.report_filepath
        report_dir = os.path.dirname(report_filepath)
        create_directories([report_dir])

        with open(report_filepath, "w") as report_file:
            json.dump(report, report_file, indent=6)
        return report

    def save_data_drift_report_page_path(self):
        dashboard = Dashboard(tabs=[DataDriftTab()])
        train_df, test_df = self.get_train_test_df()
        dashboard.calculate(train_df, test_df)

        report_page_filepath = self.data_validation_config.report_page_filepath
        report_page_dir = os.path.dirname(report_page_filepath)
        create_directories([report_page_dir])

        dashboard.save(report_page_filepath)

    def initiate_data_validation(self):
        self.is_train_test_df_available()
        self.vlaidation_datasets_schema()
        self.save_data_drift_report_page_path()
        self.get_and_save_data_drift_report()

        data_validation_artifact = DataValidationArtifact(
            report_file=self.data_validation_config.report_filepath,
            report_page_file=self.data_validation_config.report_page_filepath,
            schema_filepath=self.data_validation_config.schema_filepath,
            is_validated=True,
        )
        return data_validation_artifact
