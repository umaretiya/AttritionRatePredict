from attritionRate.components.data_ingestion import DataIngestion
from attritionRate.components.data_validation import DataValidation
from attritionRate.components.data_transformation import DataTransformation
from attritionRate.components.model_training import ModelTrainer
from attritionRate.components.model_evaluation import ModelEvaluation
from attritionRate.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainingConfig,
)
from attritionRate.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelTrainingArtifact,
)
from attritionRate.constants import CONFIG_FILE_PATH
from attritionRate.config.configuration import Configuration

conf = Configuration(config_filepath=CONFIG_FILE_PATH)
ingestion_config = conf.get_data_ingestion_config()
valid_config = conf.get_data_validation_config()
trans_config = conf.get_data_transformation_config()
model_train_config = conf.get_model_training_config()
model_eval_config = conf.get_model_evaluation_config()

ingest_config = DataIngestion(data_ingestion_config=ingestion_config)
ingest_arti = ingest_config.initiate_data_ingestion()

valid = DataValidation(ingest_arti, valid_config)
valid_arti = valid.initiate_data_validation()

trans_conf = DataTransformation(ingest_arti, valid_arti, trans_config)
trans_init = trans_conf.initiate_data_transformation()

model_train = ModelTrainer(
    model_trainer_config=model_train_config, data_transformation_artifact=trans_init
)
model_init = model_train.initiate_model_training()

model_eval = ModelEvaluation(
        model_trainer_artifact = model_init,
        model_evaluation_config= model_eval_config,
        data_ingestion_artifact = ingest_arti,
        data_validation_artifact=valid_arti,
        )
model_eval_init = model_eval.initiate_model_evaluation()

print(model_train)
print(model_init)
