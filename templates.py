import os , logging
from pathlib import Path 

formater = '[%(asctime)s]: %(filename)s: %(message)s'

logging.basicConfig(level=logging.INFO, format=formater)

project_name = "attritionRate"

list_of_files = [
    '.github/workflows/.gitkeep',
    '.github/workflows/CI.yml',
    f"project/{project_name}/__init__.py",
    f"project/{project_name}/pipeline/__init__.py",
    f"project/{project_name}/pipeline/st_01_data_ingestion.py",
    f"project/{project_name}/pipeline/st_02_data_transformation.py",
    f"project/{project_name}/pipeline/st_03_model_training.py",
    f"project/{project_name}/pipeline/st_04_model_evaluation.py",
    f"project/{project_name}/config/__init__.py",
    f"project/{project_name}/config/configuration.py",
    f"project/{project_name}/entity/__init__.py",
    f"project/{project_name}/entity/config_entity.py",
    f"project/{project_name}/components/__init__.py",
    f"project/{project_name}/components/data_ingestion.py",
    f"project/{project_name}/components/data_transformation.py",
    f"project/{project_name}/components/model_training.py",
    f"project/{project_name}/components/model_evaluation.py",
    f"project/{project_name}/utils/__init__.py",
    f"project/{project_name}/utils/common.py",
    f"project/{project_name}/constants/__init__.py",
    "tests/__init__.py",
    "tests/data/.gitkeep",
    "tests/unit/__init__.py",
    "tests/unit/test_unit.py",
    "tests/integration/__init__.py",
    "tests/integration/test_inti.py",
    "research/study.ipynb",
    "configs/config.yaml",
    "configs/schema.yaml",
    "configs/model.yaml",
    ".dvcignore",
    "dvc.yaml",
    "params.yaml",
    "setup.cfg",
    "setup.py",
    "tox.ini",
    "pyproject.toml",
    "requirements_dev.txt",
    "init_setup.sh",
    "README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")
    
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, 'w') as f:
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")