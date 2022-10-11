from attritionRate.utils import create_directories
from attritionRate.entity import DataIngestionConfig
from attritionRate.entity.artifact_entity import DataIngestionArtifact
import pandas as pd

import shutil
import os
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.config = data_ingestion_config

    def raw_data_ingestion(self):
        sourcefile = self.config.source_file
        dest_dir = self.config.dest_dir
        create_directories([dest_dir])
        shutil.copy(sourcefile, dest_dir)
        raw_data_path = os.path.join(dest_dir, os.listdir(dest_dir)[0])
        return raw_data_path

    def raw_data_spliting_train_test(self):
        # file_path = os.path.join(self.config.dest_dir, os.listdir(self.config.dest_dir)[0])
        raw_data_path = self.raw_data_ingestion()
        filename = "Table_1.csv"
        df = pd.read_csv(raw_data_path)

        new_columns = []
        for i in df.columns:
            m = (
                i.strip()
                .replace(" ", "_")
                .lower()
                .replace("/", "_")
                .replace(".", "")
                .replace("(", "")
                .replace(")", "")
            )
            new_columns.append(m)
        new_columns
        df.columns = new_columns

        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
        create_directories([self.config.train_data, self.config.test_data])
        train_filepath = os.path.join(self.config.train_data, filename)
        test_filepath = os.path.join(self.config.test_data, filename)

        train_df.to_csv(train_filepath, index=False)
        test_df.to_csv(test_filepath, index=False)

        data_ingestion_artifact = DataIngestionArtifact(
            train_data=train_filepath,
            test_data=test_filepath,
        )
        return data_ingestion_artifact

    def initiate_data_ingestion(self):
        return self.raw_data_spliting_train_test()
