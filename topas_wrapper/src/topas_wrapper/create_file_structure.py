from pathlib import Path
import shutil
from topas_wrapper.input_constants import EnergyUnit

EXPERIMENTS_FOLDER_LOCATION = "../../experiments"

def create_file_structure(experiment_name: str, relative_filepath: str, overwrite: bool=False):
    mod_path = Path(__file__).parent
    experiment_folder = (mod_path / relative_filepath / experiment_name).resolve()
    if experiment_folder.exists() and not overwrite:
        raise FileExistsError("An experiment with this name already exists. Rename experiment or set overwrite parameter to true.") #TODO allow UI here for overwriting
    if experiment_folder.exists() and not experiment_folder.is_dir():
        raise FileExistsError(f"You have an unexpected file with the experiment name -> {experiment_name} at location -> {experiment_folder}. \nPlease remove it.")
    if experiment_folder.exists():
        print(f"Overwriting -> {experiment_folder}")
        shutil.rmtree(experiment_folder)

    scripts_folder = (experiment_folder / "scripts").resolve()
    data_folder = (experiment_folder / "data").resolve()
    analysis_folder = (experiment_folder / "analysis").resolve()

    scripts_folder.mkdir(parents=True, exist_ok=False)
    data_folder.mkdir(exist_ok=False)
    analysis_folder.mkdir(exist_ok=False)
    return scripts_folder, data_folder, analysis_folder


def create_filename(beam_energy: float, beam_energy_units: EnergyUnit, number_of_histories: int):
    beam_energy_string = f"{beam_energy:.2f}"
    beam_energy_string = beam_energy_string.replace('.', 'p')
    filename = f"beam_energy_{beam_energy_string}_{beam_energy_units.value}_number_of_histories_{number_of_histories}.txt"
    return filename


def create_output_filepath(data_folder: str, beam_energy: float, beam_energy_units: EnergyUnit, number_of_histories: int):
    beam_energy_string = f"{beam_energy:.2f}"
    beam_energy_string = beam_energy_string.replace('.', 'p')
    filename = f"beam_energy_{beam_energy_string}_{beam_energy_units.value}_number_of_histories_{number_of_histories}"
    output_filepath = (data_folder / filename).resolve()
    return output_filepath