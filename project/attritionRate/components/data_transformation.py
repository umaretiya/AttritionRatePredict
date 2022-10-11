from attritionRate.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
)
from attritionRate.entity.config_entity import (
    DataTransformationConfig,
)
from attritionRate.utils import read_yaml, create_directories, save_bin, load_data

import numpy as np

import os

from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


class DataTransformation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    def get_data_transformer_object(self):
        schema_filepath = self.data_validation_artifact.schema_filepath
        dataset_schema = read_yaml(schema_filepath)

        cat_columns = dataset_schema.categorical_columns
        num_columns = dataset_schema.numerical_columns

        num_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="mean")),
                ("sclaer", StandardScaler()),
            ]
        )

        cat_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "ordinal",
                    OrdinalEncoder(
                        handle_unknown="use_encoded_value", unknown_value=-1
                    ),
                ),
                ("scaler", StandardScaler(with_mean=False)),
            ]
        )

        preprocessing = ColumnTransformer(
            [
                ("numerical", num_pipeline, num_columns),
                ("categorical", cat_pipeline, cat_columns),
            ]
        )
        print("num_column", num_columns)
        print("cat_columns", cat_columns)
        return preprocessing

    def initiate_data_transformation(self):
        preprocessing_obj = self.get_data_transformer_object()

        schema_filepath = self.data_validation_artifact.schema_filepath
        train_data_filepath = self.data_ingestion_artifact.train_data
        test_data_filepath = self.data_ingestion_artifact.test_data

        schema = read_yaml(schema_filepath)
        train_df = load_data(train_data_filepath, schema_filepath)
        test_df = load_data(test_data_filepath, schema_filepath)
        # train_df = pd.read_csv(train_data_filepath)
        # test_df = pd.read_csv(test_data_filepath)

        target_column = schema.target_column

        feature_train_df = train_df.drop([target_column], axis=1)
        feature_test_df = test_df.drop([target_column], axis=1)
        feature_train_df = train_df
        feature_test_df = test_df

        target_train_df = train_df[target_column].map(lambda x: 1 if x == "Stay" else 0)
        target_test_df = test_df[target_column].map(lambda x: 1 if x == "Stay" else 0)

        input_feature_train_arr = preprocessing_obj.fit_transform(feature_train_df)
        input_feature_test_arr = preprocessing_obj.transform(feature_test_df)

        train_arr = np.c_[input_feature_train_arr, np.array(target_train_df)]
        test_arr = np.c_[input_feature_test_arr, np.array(target_test_df)]

        train_dirpath = self.data_transformation_config.transformed_train_dir
        test_dirpath = self.data_transformation_config.transformed_test_dir

        train_filename = os.path.basename(train_data_filepath).replace(".csv", ".npz")
        test_filename = os.path.basename(test_data_filepath).replace(".csv", ".npz")

        create_directories([train_dirpath, test_dirpath])
        transformed_train_datapath = os.path.join(train_dirpath, train_filename)
        transformed_test_datapath = os.path.join(test_dirpath, test_filename)

        with open(transformed_train_datapath, "wb") as trainfile:
            np.save(trainfile, train_arr)

        with open(transformed_test_datapath, "wb") as testfile:
            np.save(testfile, test_arr)

        preprocessing_obj_filepath = (
            self.data_transformation_config.preprocessed_obj_path
        )
        create_directories([os.path.dirname(preprocessing_obj_filepath)])
        save_bin(preprocessing_obj, preprocessing_obj_filepath)

        data_transformation_artifact = DataTransformationArtifact(
            train_data=transformed_train_datapath,
            test_data=transformed_test_datapath,
            preprocessed_obj_path=preprocessing_obj_filepath,
        )
        return data_transformation_artifact
