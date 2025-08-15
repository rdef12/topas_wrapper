from pathlib import Path
import shutil

EXPERIMENTS_FOLDER_LOCATION = "../../experiments"

def create_file_structure(experiment_name: str, relative_filepath: str, overwrite: bool=False) -> Path:
    mod_path = Path(__file__).parent
    experiment_folder = (mod_path / relative_filepath / experiment_name).resolve()
    if experiment_folder.exists() and not overwrite:
        raise FileExistsError("An experiment with this name already exists. Rename experiment or set overwrite parameter to true.") #TODO allow UI here for overwriting
    if experiment_folder.exists() and not experiment_folder.is_dir():
        raise FileExistsError(f"You have an unexpected file with the experiment name -> {experiment_name} at location -> {experiment_folder}. \nPlease remove it.")
    if experiment_folder.exists():
        # print(experiment_folder)
        shutil.rmtree(experiment_folder)

    scripts_folder = (experiment_folder / "scripts").resolve()
    data_folder = (experiment_folder / "data").resolve()
    analysis_folder = (experiment_folder / "analysis").resolve()

    scripts_folder.mkdir(parents=True, exist_ok=False)
    data_folder.mkdir(exist_ok=False)
    analysis_folder.mkdir(exist_ok=False)
    return scripts_folder, data_folder, analysis_folder