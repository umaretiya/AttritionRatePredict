from attritionRate.components.data_ingestion import DataIngestion

from attritionRate.constants import CONFIG_FILE_PATH
from attritionRate.config.configuration import Configuration

name = "data_ingestion"

conf = Configuration(config_filepath=CONFIG_FILE_PATH)
ingestion_config = conf.get_data_ingestion_config()
valid_config = conf.get_data_validation_config()
trans_config = conf.get_data_transformation_config()
model_train_config = conf.get_model_training_config()

ingest_config = DataIngestion(data_ingestion_config=ingestion_config)
ingest_arti = ingest_config.initiate_data_ingestion()

# valid = DataValidation(ingest_arti,valid_config)
# valid_arti = valid.initiate_data_validation()

# trans_conf = DataTransformation(ingest_arti, valid_arti, trans_config)
# trans_init = trans_conf.initiate_data_transformation()

# model_train = ModelTrainer(model_trainer_config=model_train_config, data_transformation_artifact=trans_init)
# model_init = model_train.initiate_model_training()
# print(model_train)
# print(model_init)
