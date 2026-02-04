# import os
# from pathlib import Path
# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="[%(asctime)s]: %(message)s"
# )

# project_name = "carDirection"

# list_of_files = [
#     ".github/workflows/.gitkeep",
#     "data/.gitkeep",
#     "docs/.gitkeep",

#     f"{project_name}/__init__.py",

#     f"{project_name}/components/__init__.py",
#     f"{project_name}/components/data_ingestion.py",
#     f"{project_name}/components/data_validation.py",
#     f"{project_name}/components/model_trainer.py",
#     f"{project_name}/components/model_pusher.py",

#     f"{project_name}/configuration/__init__.py",
#     f"{project_name}/configuration/s3_operations.py",

#     f"{project_name}/constant/__init__.py",
#     f"{project_name}/constant/training_pipeline/__init__.py",
#     f"{project_name}/constant/application.py",

#     f"{project_name}/entity/__init__.py",
#     f"{project_name}/entity/artifacts_entity.py",
#     f"{project_name}/entity/config_entity.py",

#     f"{project_name}/exception/__init__.py",

#     f"{project_name}/logger/__init__.py",

#     f"{project_name}/pipeline/__init__.py",
#     f"{project_name}/pipeline/training_pipeline.py",

#     f"{project_name}/utils/__init__.py",
#     f"{project_name}/utils/main_utils.py",

#     "template/index.html",
#     ".dockerignore",
#     "app.py",
#     "Dockerfile",
#     "requirements.txt",
#     "setup.py"
# ]

# for filepath in list_of_files:
#     filepath = Path(filepath)
#     filedir = filepath.parent

#     # Create directories if they don't exist
#     if filedir != Path("."):
#         os.makedirs(filedir, exist_ok=True)
#         logging.info(f"Created directory: {filedir} for the file {filepath.name}")

#     # If a directory exists with the same name as the file, remove it
#     if filepath.exists() and filepath.is_dir():
#         logging.warning(f"{filepath} exists as a directory. Removing to create a file.")
#         os.rmdir(filepath)

#     # Create the file if it doesn't exist
#     if not filepath.exists():
#         with open(filepath, "w") as f:
#             pass
#         logging.info(f"Created empty file: {filepath}")
#     else:
#         logging.info(f"File already exists: {filepath}")




import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "signLanguage"


list_of_files = [
    "data/.gitkeep",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/s3_operations.py",
    f"{project_name}/constant/__init__.py",
    f"{project_name}/constant/training_pipeline/__init__.py",
    f"{project_name}/constant/application.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/artifacts_entity.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    "template/index.html",
    ".dockerignore",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py"


]


for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    
    if(not os.path.exists(filename)) or (os.path.getsize(filename) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f"Creating empty file: {filename}")

    
    else:
        logging.info(f"{filename} is already created")