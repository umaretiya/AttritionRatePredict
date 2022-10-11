from typing import List
from attritionRate.entity.artifact_entity import (
    DataTransformationArtifact,
    MetricInfoArtifact,
    GridSearchBestModel,
    ModelTrainingArtifact,
)
from attritionRate.utils import load_bin, save_object
from attritionRate.components.model_factory import evaluate_classifier, ModelFactory
from attritionRate.entity.config_entity import ModelTrainingConfig

import numpy as np


class EstimatorMain:
    def __init__(self, preprocessing_obj, trained_model_object):
        self.preprocessing_object = preprocessing_obj
        self.trained_model_object = trained_model_object

    def predict(self, X):
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainingConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        self.model_trainer_config = model_trainer_config
        self.data_transforamtion_artifact = data_transformation_artifact

    def initiate_model_training(self):
        transformed_train_filepath = self.data_transforamtion_artifact.train_data
        with open(transformed_train_filepath, "rb") as tafile:
            train_arr = np.load(tafile)

        transformed_test_filepath = self.data_transforamtion_artifact.test_data
        with open(transformed_test_filepath, "rb") as tsfile:
            test_arr = np.load(tsfile)

        x_train, y_train, x_test, y_test = (
            train_arr[:, :-1],
            train_arr[:, -1],
            test_arr[:, :-1],
            test_arr[:, -1],
        )
        base_accuracy = 0.5
        model_config_filepath = self.model_trainer_config.model_config_filepath

        model_factory = ModelFactory(model_config_path=model_config_filepath)

        best_model = model_factory.get_best_model(
            X=x_train, y=y_train, base_accuracy=base_accuracy
        )
        print(best_model)
        grid_search_best_model_list: List[
            GridSearchBestModel
        ] = model_factory.grid_search_best_model_list

        model_list = [model.best_model for model in grid_search_best_model_list]

        metric_info: MetricInfoArtifact = evaluate_classifier(
            model_list=model_list,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            base_accuracy=base_accuracy,
        )
        pre_pro_path = self.data_transforamtion_artifact.preprocessed_obj_path
        preprocessing_obj = load_bin(pre_pro_path)
        model_object = metric_info.model_object

        trained_model_filepath = self.model_trainer_config.model_train_filepath

        main_model = EstimatorMain(
            preprocessing_obj=preprocessing_obj, trained_model_object=model_object
        )
        save_object(file_path=trained_model_filepath, obj=main_model)

        model_trainer_artifact = ModelTrainingArtifact(
            trained_model_path=trained_model_filepath,
            train_accuracy=metric_info.train_accuracy,
            test_acuuracy=metric_info.test_accuracy,
            model_accuracy=metric_info.model_accuracy,
        )
        return model_trainer_artifact
