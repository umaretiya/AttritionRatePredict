from attritionRate.entity.config_entity import ModelEvaluationConfig
from attritionRate.entity.artifact_entity import (
    ModelEvaluationArtifact,
    DataIngestionArtifact,
    DataValidationArtifact,
    ModelTrainingArtifact,
)
import shutil
import os
import numpy as np
from attritionRate.utils import read_yaml, write_yaml, load_object, load_data
from attritionRate.components.model_factory import evaluate_classifier


class ModelEvaluation:
    def __init__(
        self,
        model_trainer_artifact: ModelTrainingArtifact,
        model_evaluation_config: ModelEvaluationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact,
    ):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifact = model_trainer_artifact
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact

    def get_best_model(self):
        model = None
        model_evaluation_filepath = (
            self.model_evaluation_config.model_evaluation_filepath
        )
        if not os.path.exists(model_evaluation_filepath):
            write_yaml(file_path=model_evaluation_filepath, data=dict())
            return model
        
        model_eval_file_content = read_yaml(model_evaluation_filepath)
        
        model_eval_file_content = (
            dict() if model_eval_file_content is None else model_eval_file_content
        )

        if "best_model" not in model_eval_file_content:
            return model

        model = load_object(
            file_path=model_eval_file_content["best_model"]["model_path"]
        )
        return model

    def update_evaluation_report(
        self, model_evaluation_artifact: ModelEvaluationArtifact
    ):
        eval_filepath = self.model_evaluation_config.model_evaluation_filepath
        model_eval_content = read_yaml(eval_filepath)
        model_eval_content = (
            dict() if model_eval_content is None else model_eval_content
        )

        previous_best_model = None
        if "best_model" in model_eval_content:
            previous_best_model = model_eval_content["best_model"]

        eval_result = {
            "best_model": {"model_path": model_evaluation_artifact.evaluated_model_path}
        }

        if previous_best_model is not None:
            model_history = {
                self.model_evaluation_config.time_stamp: previous_best_model
            }
            if "history" not in model_eval_content:
                history = {"history": model_history}
                eval_result.update(history)
            else:
                model_eval_content["history"].update(model_history)

        model_eval_content.update(eval_result)
        write_yaml(file_path=eval_filepath, data=model_eval_content)

    def initiate_model_evaluation(self):
        trained_model_filepath = self.model_trainer_artifact.trained_model_path
        trained_model_object = load_object(trained_model_filepath)

        train_filepath = self.data_ingestion_artifact.train_data
        test_filepath = self.data_ingestion_artifact.test_data

        schema_filepath = self.data_validation_artifact.schema_filepath

        train_df = load_data(file_path=train_filepath, schema_filepath=schema_filepath)
        test_df = load_data(file_path=test_filepath, schema_filepath=schema_filepath)
        
        schema_content = read_yaml(schema_filepath)
        target_column = schema_content.target_column

        train_target_arr = np.array(train_df[target_column].map(lambda x: 1 if x=='Stay' else 0))
        test_target_arr = np.array(test_df[target_column].map(lambda x: 1 if x=='Stay' else 0))
        
        train_df[target_column] = train_df[target_column].map(lambda x: 1 if x=='Stay' else 0)
        test_df[target_column] = test_df[target_column].map(lambda x: 1 if x=='Stay' else 0)
        
        train_df.drop(target_column, axis=1, inplace=True)
        test_df.drop(target_column, axis=1, inplace=True)

        model = self.get_best_model()
        print("get best Model: ", model)
        export_dir = self.model_evaluation_config.export_dir_path
        evaluated_model_file_path = (
            self.model_evaluation_config.model_evaluation_filepath
        )
        print(evaluated_model_file_path)
        # model_file_name = os.path.basename(evaluated_model_file_path)
        model_file_name = "model.pkl"
        exported_model_filepath = os.path.join(export_dir, model_file_name)
        os.makedirs(export_dir, exist_ok=True)
        
        shutil.copy(src=trained_model_filepath, dst=exported_model_filepath)

        if model is None:
            model_evaluation_artifact = ModelEvaluationArtifact(
                evaluated_model_path=trained_model_filepath,
                is_model_accepted=True,
                exported_model_path=exported_model_filepath,
                is_model_pusher=True,
            )
            self.update_evaluation_report(
                model_evaluation_artifact=model_evaluation_artifact
            )

        model_list = [trained_model_object]
        metric_info_artifact = evaluate_classifier(
            model_list=model_list,
            x_train=train_df,
            x_test=test_df,
            y_train=train_target_arr,
            y_test=test_target_arr,
            base_accuracy=0.6,
        )
        if metric_info_artifact is None:
            response = model_evaluation_artifact = ModelEvaluationArtifact(
                evaluated_model_path=trained_model_filepath,
                is_model_accepted=False,
                exported_model_path=exported_model_filepath,
                is_model_pusher=True,
            )
            return response

        if metric_info_artifact.index_number == 1:
            model_evaluation_artifact = ModelEvaluationArtifact(
                evaluated_model_path=trained_model_filepath,
                is_model_accepted=True,
                exported_model_path=exported_model_filepath,
                is_model_pusher=True,
            )
            self.update_evaluation_report(
                model_evaluation_artifact=model_evaluation_artifact
            )
        else:
            model_evaluation_artifact = ModelEvaluationArtifact(
                evaluated_model_path=trained_model_filepath,
                is_model_accepted=False,
                exported_model_path=exported_model_filepath,
                is_model_pusher=True,
            )
            return model_evaluation_artifact
