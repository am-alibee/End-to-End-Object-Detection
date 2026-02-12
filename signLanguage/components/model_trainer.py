

import os
import sys
import yaml
import zipfile
import shutil
import subprocess


from signLanguage.utils import read_yaml
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifacts_entity import ModelTrainerArtifacts


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig ):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        logging.info(f"Entered initiate_model_trainer method of ModelTrainer")

        try:
            # ------unzip dataset ----------
            zip_path = 'signLanguage.zip'
            if os.path.exists(zip_path):
                logging.info(("Unzipping the data"))
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(".")
                os.remove(zip_path)

            # read number of classes
            with open("data.yaml", "r") as file:
                num_classes = int(yaml.safe_load(file)["nc"])

            # prepare yolo model config 
            model_name = self.model_trainer_config.weight_name.split(".")[0]
            logging.info(f"Model config base {model_name}")

            base_cfg_path = os.path.join(
                "yolov5", "models", f"{model_name}.yaml"
            )

            custom_cfg_path = os.path.join(
                "yolov5", "models", f"custom_{model_name}.yaml"
            )

            config = read_yaml(base_cfg_path)
            config["nc"] = num_classes

            with open(custom_cfg_path, "w") as f:
                yaml.dump(config, f, sort_keys=False)

            # train yolov5
            train_command = [
                sys.executable,
                "train.py",
                "--img", "416",
                "--batch", str(self.model_trainer_config.batch_size),
                "--epochs", str(self.model_trainer_config.no_epochs),
                "--data", "../data.yaml",
                "--cfg", f"models/custom_{model_name}.yaml",
                "--weights", self.model_trainer_config.weight_name,
                "--name", "yolo_results",
                "--exist-ok",
                "--cache",
                "--device", "cpu",
                "--workers", "0"
            ]

            logging.info("Started yolov5 training")
            subprocess.run(train_command, cwd="yolov5", check=True)

            # -------- save trained model-------------
            best_model_path = os.path.join(
                "yolov5", "runs", "train", "yolo_results", "weights", "best.pt"
            )

            if not os.path.exists(best_model_path):
                raise FileNotFoundError("best.pt not found after training")
            
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)

            final_model_path = os.path.join(
                self.model_trainer_config.model_trainer_dir, "best.pt"
            )

            shutil.copy(best_model_path, final_model_path)

            # --------- clean up-------------

            shutil.rmtree(os.path.join("yolov5", "runs"), ignore_errors=True)

            for folder in ["train", "test", "valid"]:
                if os.path.exists(folder):
                    shutil.rmtree(folder, ignore_errors=True)

            if os.path.exists("data.yaml"):
                os.remove("data.yaml")

            # ------------ artifact -------------
            artifact = ModelTrainerArtifacts(
                trained_model_file_path=final_model_path
            )

            logging.info("Model Training Completed Successfully")
            logging.info(f"Model Trainer Artifact: {artifact}")

            return artifact
        
        except Exception as e:
            raise SignException(e, sys)