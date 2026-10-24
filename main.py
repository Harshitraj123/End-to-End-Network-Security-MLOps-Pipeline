import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


if __name__ == "__main__":
    try:
        # Initialize the training pipeline configuration
        training_pipeline_config = TrainingPipelineConfig()

        # ==================== DATA INGESTION ====================

        logging.info("Starting Data Ingestion")

        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config
        )

        data_ingestion = DataIngestion(
            data_ingestion_config
        )

        data_ingestion_artifact = (
            data_ingestion.initiate_data_ingestion()
        )

        logging.info("Data Ingestion completed successfully")
        print(data_ingestion_artifact)

        # ==================== DATA VALIDATION ====================

        logging.info("Starting Data Validation")

        data_validation_config = DataValidationConfig(
            training_pipeline_config
        )

        data_validation = DataValidation(
            data_ingestion_artifact,
            data_validation_config,
        )

        data_validation_artifact = (
            data_validation.initiate_data_validation()
        )

        logging.info("Data Validation completed successfully")
        print(data_validation_artifact)

        # ==================== DATA TRANSFORMATION ====================

        logging.info("Starting Data Transformation")

        data_transformation_config = DataTransformationConfig(
            training_pipeline_config
        )

        data_transformation = DataTransformation(
            data_validation_artifact,
            data_transformation_config,
        )

        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        logging.info("Data Transformation completed successfully")
        print(data_transformation_artifact)

        # ==================== MODEL TRAINING ====================

        logging.info("Starting Model Training")

        model_trainer_config = ModelTrainerConfig(
            training_pipeline_config
        )

        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )

        model_trainer_artifact = (
            model_trainer.initiate_model_trainer()
        )

        logging.info("Model Training completed successfully")
        print(model_trainer_artifact)

        logging.info("Network Security training pipeline completed successfully")

    except Exception as e:
        logging.exception("Network Security training pipeline failed")
        raise NetworkSecurityException(e, sys) from e