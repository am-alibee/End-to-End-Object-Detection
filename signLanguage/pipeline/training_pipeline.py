import sys
import os

from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.components.data_ingestion import DataIngestion
from signLanguage.components.data_validation import DataValidation
from signLanguage.components.model_trainer import ModelTrainer
from signLanguage.components.model_pusher import ModelPusher

from signLanguage.configuration.s3_operations import S3Operation

from signLanguage.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    ModelPusherConfig
)

from signLanguage.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    ModelTrainerArtifacts,
    ModelPusherArtifact
)


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_pusher_config = ModelPusherConfig()

    # ---------------- DATA INGESTION ----------------
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered start_data_ingestion method")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Exited start_data_ingestion method")
            return artifact

        except Exception as e:
            raise SignException(e, sys)

    # ---------------- DATA VALIDATION ----------------
    def start_data_validation(
        self,
        data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        try:
            logging.info("Entered start_data_validation method")

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )

            artifact = data_validation.initiate_data_validation()

            logging.info("Exited start_data_validation method")
            return artifact

        except Exception as e:
            raise SignException(e, sys)

    # ---------------- MODEL TRAINING ----------------
    def start_model_trainer(self) -> ModelTrainerArtifacts:
        try:
            logging.info("Entered start_model_trainer method")

            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config
            )

            artifact = model_trainer.initiate_model_trainer()

            logging.info("Exited start_model_trainer method")
            return artifact

        except Exception as e:
            raise SignException(e, sys)

    # ---------------- MODEL PUSHER ----------------
    def start_model_pusher(
        self,
        model_trainer_artifact: ModelTrainerArtifacts,
        s3_operation: S3Operation
    ) -> ModelPusherArtifact:
        try:
            logging.info("Entered start_model_pusher method")

            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_trainer_artifact=model_trainer_artifact,
                s3=s3_operation
            )

            artifact = model_pusher.initiate_model_pusher()

            logging.info("Exited start_model_pusher method")
            return artifact

        except Exception as e:
            raise SignException(e, sys)

    # ---------------- PIPELINE RUNNER ----------------
    def run_pipeline(self) -> None:
        try:
            logging.info("Training pipeline started")

            # 1. Data ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # 2. Data validation
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            if not data_validation_artifact.validation_status:
                raise Exception("Data validation failed")

            # 3. Model training
            model_trainer_artifact = self.start_model_trainer()

            # 4. Model push to S3
            s3_operation = S3Operation()
            self.start_model_pusher(
                model_trainer_artifact=model_trainer_artifact,
                s3_operation=s3_operation
            )

            logging.info("Training pipeline completed successfully")

        except Exception as e:
            raise SignException(e, sys)
