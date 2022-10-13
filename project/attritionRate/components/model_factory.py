import importlib
from typing import List
from sklearn.metrics import accuracy_score, f1_score
from attritionRate.entity.artifact_entity import GridSearchBestModel, MetricInfoArtifact
from attritionRate.entity.config_entity import InitializedModel
from attritionRate.utils import read_yaml
from attritionRate.constants import MODEL_FILE_PATH


def evaluate_classifier(
    model_list: list, x_train, y_train, x_test, y_test, base_accuracy: float = 0.6
):
    index_number = 0
    metric_info_artifact = None
    for model in model_list:
        y_train_pred = model.predict(x_train)
        y_test_pred = model.predict(x_test)

        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)

        train_f1_score = f1_score(y_train, y_train_pred)
        test_f1_score = f1_score(y_test, y_test_pred)

        model_accuracy = (2 * (train_acc * test_acc)) / (train_acc + test_acc)

        if model_accuracy >= base_accuracy:
            metric_info_artifact = MetricInfoArtifact(
                model_name=str(model),
                model_object=model,
                train_accuracy=train_acc,
                test_accuracy=test_acc,
                train_f1_score=train_f1_score,
                test_f1_score=test_f1_score,
                model_accuracy=model_accuracy,
                index_number=index_number,
            )
    index_number += 1
    if metric_info_artifact is None:
        print("No model found with higher than base accuracy")
    return metric_info_artifact


class ModelFactory:
    def __init__(self, model_config_path=MODEL_FILE_PATH):
        self.model_config = read_yaml(model_config_path)
        print(self.model_config)
        self.grid_search_module = self.model_config.grid_search.module  # ['module']
        self.grid_search_class = self.model_config.grid_search["class"]
        self.grid_search_property_data = self.model_config.grid_search["params"]
        self.model_initialization_config = self.model_config.model_selection

    @staticmethod
    def class_for_name(module_name: str, class_name: str):
        module = importlib.import_module(module_name)
        class_ref = getattr(module, class_name)
        return class_ref

    @staticmethod
    def update_property_of_class(instance_ref: object, property_data: dict):
        if not isinstance(property_data, dict):
            raise Exception("property data required for Dictionary")

        for key, val in property_data.items():
            setattr(instance_ref, key, val)
        return instance_ref

    def execute_gridsearch_operation(
        self, initialized_model: InitializedModel, input_feature, output_feature
    ):
        grid_search_cv_ref = ModelFactory.class_for_name(
            module_name=self.grid_search_module, class_name=self.grid_search_class
        )
        grid_search_cv = grid_search_cv_ref(
            estimator=initialized_model.model,
            param_grid=initialized_model.param_grid_search,
        )
        grid_searchCV = ModelFactory.update_property_of_class(
            grid_search_cv, self.grid_search_property_data
        )

        message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__} Started." {"<<"*30}'
        print(message)
        grid_searchCV.fit(input_feature, output_feature)
        message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__} Completed." {"<<"*30}'
        print(message)
        grid_searched_best_model = GridSearchBestModel(
            model_serial_number=initialized_model.model_serial_number,
            model=initialized_model.model,
            best_model=grid_searchCV.best_estimator_,
            best_parameters=grid_searchCV.best_params_,
            best_score=grid_searchCV.best_score_,
        )
        return grid_searched_best_model

    def get_initialized_model_list(self):
        initialized_model_list = []
        for model_serial_number in self.model_initialization_config.keys():
            model_initialized_config = self.model_initialization_config[
                model_serial_number
            ]
            model_obj_ref = ModelFactory.class_for_name(
                module_name=model_initialized_config["module"],
                class_name=model_initialized_config["class"],
            )
            model_obj = model_obj_ref()

            if "params" in model_initialized_config:
                model_obj_property_data = model_initialized_config["params"]
                model = ModelFactory.update_property_of_class(
                    instance_ref=model_obj, property_data=model_obj_property_data
                )

            param_gird_search = model_initialized_config["search_param_grid"]
            model_name = f"{model_initialized_config['module']}.{model_initialized_config['class']}()"

            model_initialization_config = InitializedModel(
                model_serial_number=model_serial_number,
                model=model,
                param_grid_search=param_gird_search,
                model_name=model_name,
            )
            initialized_model_list.append(model_initialization_config)

        self.initialized_model_list = initialized_model_list
        return self.initialized_model_list

    def initiate_best_parameter_search_for_initialized_model(
        self, initialized_model: InitializedModel, input_feature, output_feature
    ):
        return self.execute_gridsearch_operation(
            initialized_model=initialized_model,
            input_feature=input_feature,
            output_feature=output_feature,
        )

    def initiate_best_parameter_search_for_initialized_models(
        self,
        initialized_model_list: List[InitializedModel],
        input_feature,
        output_feature,
    ):
        self.grid_search_best_model_list = []
        for initialized_model in initialized_model_list:
            grid_search_best_model = (
                self.initiate_best_parameter_search_for_initialized_model(
                    initialized_model=initialized_model,
                    input_feature=input_feature,
                    output_feature=output_feature,
                )
            )
            self.grid_search_best_model_list.append(grid_search_best_model)
        return self.grid_search_best_model_list

    def get_best_model(self, X, y, base_accuracy=0.6):
        initialized_model_list = self.get_initialized_model_list()
        grid_search_best_model_list = (
            self.initiate_best_parameter_search_for_initialized_models(
                initialized_model_list=initialized_model_list,
                input_feature=X,
                output_feature=y,
            )
        )
        return ModelFactory.get_best_model_from_grid_searched_best_model_list(
            grid_search_best_model_list=grid_search_best_model_list,
            base_accuracy=base_accuracy,
        )

    @staticmethod
    def get_best_model_from_grid_searched_best_model_list(
        grid_search_best_model_list: List[GridSearchBestModel], base_accuracy=0.6
    ):
        best_model = None
        for grid_search_best_model in grid_search_best_model_list:
            if base_accuracy < grid_search_best_model.best_score:
                base_accuracy = grid_search_best_model.best_score
                best_model = grid_search_best_model.best_model
        if not best_model:
            raise Exception(
                f"Non of the model has accuracy greater then: {base_accuracy}"
            )

        return best_model

    @staticmethod
    def get_model_details(model_details: List[InitializedModel], model_serial_number):
        for model_data in model_details:
            if model_data.model_serial_number == model_serial_number:
                return model_data
