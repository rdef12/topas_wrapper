import os
import subprocess
import json
from typing import List
from pathlib import Path
from itertools import product
from topas_wrapper.get_data import locate_experiment_config_file
from topas_wrapper.get_data import load_experiment_parameters, ParticleSource, ExperimentPhysicsList, Scorer, ExperimentParameters
from topas_wrapper.create_file_structure import create_file_structure, create_filename, create_output_filepath
from topas_wrapper.file_structure import FileStructure
from topas_wrapper.input_constants import EnergyUnit


def generate_number_of_threads_text(number_of_threads: int) -> List[str]:
    number_of_threads_text = f"i:Ts/NumberOfThreads = {number_of_threads}"
    return [number_of_threads_text]


def generate_seed_number_text(seed_number: int) -> List[str]:
    if seed_number == 0:
        return ['b:Ts/SeedFromTime = "True"']
    return [f'i:Ts/Seed = {seed_number}']


def generate_number_of_histories_text(number_of_histories: int, particle_source_component: str) -> List[str]:
    return [f"i:So/{particle_source_component}/NumberOfHistoriesInRun = {number_of_histories}"]


def load_experiment_geometry_text() -> List[str]:
    try:
        experiment_geometry_path = locate_experiment_config_file(FileStructure.GEOMETRY.value)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"EXPERIMENT_GEOMETRY.txt does not exist in the expected location. \n{e} \nRefer to the original file structure.")
    geometry_lines = experiment_geometry_path.read_text().splitlines()    
    return geometry_lines


def generate_particle_source_text(particle_source: ParticleSource, beam_energy: float, beam_energy_spread: float) -> List[str]:
    component = particle_source.component
    particle_source_text = [
        "!!!particle-source-start!!!",
        f's:So/{component}/Type = "{particle_source.type.value}"',
        f's:So/{component}/Component = "{particle_source.component}"',
        f's:So/{component}/BeamParticle = "{particle_source.beam_particle.value}"',
        f'd:So/{component}/BeamEnergy = {beam_energy:.2f} {particle_source.beam_energy_unit.value}',
        f'u:So/{component}/BeamEnergySpread = {beam_energy_spread:.2f}',
        f's:So/{component}/BeamPositionDistribution = "{particle_source.beam_position_distribution.value}"',
        f's:So/{component}/BeamPositionCutoffShape = "{particle_source.beam_position_cutoff_shape.value}"',
        f'd:So/{component}/BeamPositionCutoffX = {particle_source.beam_position_cutoff_x} {particle_source.beam_position_cutoff_x_units.value}',
        f'd:So/{component}/BeamPositionCutoffY = {particle_source.beam_position_cutoff_y} {particle_source.beam_position_cutoff_y_units.value}',
        f'd:So/{component}/BeamPositionSpreadX = {particle_source.beam_position_spread_x} {particle_source.beam_position_spread_x_units.value}',
        f'd:So/{component}/BeamPositionSpreadY = {particle_source.beam_position_spread_y} {particle_source.beam_position_spread_y_units.value}',
        f's:So/{component}/BeamAngularDistribution = "{particle_source.beam_angular_distribution.value}"',
        f'd:So/{component}/BeamAngularCutoffX = {particle_source.beam_angular_cutoff_x} {particle_source.beam_angular_cutoff_x_units.value}',
        f'd:So/{component}/BeamAngularCutoffY = {particle_source.beam_angular_cutoff_y} {particle_source.beam_angular_cutoff_y_units.value}',
        f'd:So/{component}/BeamAngularSpreadX = {particle_source.beam_angular_spread_x} {particle_source.beam_angular_spread_x_units.value}',
        f'd:So/{component}/BeamAngularSpreadY = {particle_source.beam_angular_spread_y} {particle_source.beam_angular_spread_y_units.value}',
        "!!!particle-source-end!!!"
    ]
    return particle_source_text


def generate_physics_lists_text(physics_list: ExperimentPhysicsList) -> List[str]:
    modules = physics_list.modules
    number_of_modules = len(modules)
    string_of_modules = " ".join(f'"{module}"' for module in modules)
    physics_list_text = [
        '!!!physics-lists-start!!!',
        f's:Ph/ListName = "{physics_list.list_name}"',
        f'b:Ph/ListProcesses = "{physics_list.list_processes}"',
        f's:Ph/{physics_list.list_name}/Type = "{physics_list.type}"',
        f'sv:Ph/{physics_list.list_name}/Modules = {number_of_modules} {string_of_modules}',
        f'd:Ph/{physics_list.list_name}/EMRangeMin = {physics_list.EM_range_min} {physics_list.EM_range_min_units.value}',
        f'd:Ph/{physics_list.list_name}/EMRangeMax = {physics_list.EM_range_max} {physics_list.EM_range_max_units.value}',
        '!!!physics-lists-end!!!'
    ]
    return physics_list_text


def generate_scoring_text(scorer: Scorer, data_folder: Path, beam_energy: float, beam_energy_units: EnergyUnit, number_of_histories: int) -> List[str]:
    scorer_text = [
        '!!!scorer-start!!!'
        f's:Sc/Scorer/Quantity = "{scorer.quantity.value}"',
        f's:Sc/Scorer/Component = "{scorer.component}"',
        f'b:Sc/Scorer/OutputToConsole = "False"'
    ]
    if scorer.only_include_particles_named is not None:
        number_of_particles_to_include = len(scorer.only_include_particles_named)
        string_of_particles = " ".join(f'"{particle.value}"' for particle in scorer.only_include_particles_named)
        scorer_text.append(f'sv:Sc/Scorer/OnlyIncludeParticlesNamed = {number_of_particles_to_include} {string_of_particles}')
    if scorer.x_bins is not None:
        scorer_text.append(f'i:Sc/Scorer/XBins = {scorer.x_bins}')
    if scorer.y_bins is not None:
        scorer_text.append(f'i:Sc/Scorer/YBins = {scorer.y_bins}')
    if scorer.z_bins is not None:
        scorer_text.append(f'i:Sc/Scorer/ZBins = {scorer.z_bins}')
    output_filepath = create_output_filepath(data_folder, beam_energy, beam_energy_units, number_of_histories)
    scorer_text.append(f's:Sc/Scorer/OutputFile = "{output_filepath}"')
    scorer_text.append('!!!scorer-end!!!')
    return scorer_text


def generate_script(experiment_parameters: ExperimentParameters, energy_index: int, number_of_histories_index: int, data_folder: Path) -> List[str]:
    script = []

    number_of_threads_text = generate_number_of_threads_text(experiment_parameters.number_of_threads)
    script += number_of_threads_text

    number_of_histories = experiment_parameters.numbers_of_histories[number_of_histories_index]
    number_of_histories_text = generate_number_of_histories_text(number_of_histories, experiment_parameters.particle_source.component)
    script += number_of_histories_text

    geometry_text = load_experiment_geometry_text()
    script += geometry_text

    beam_energy = experiment_parameters.particle_source.beam_energy[energy_index]
    beam_energy_spread = experiment_parameters.particle_source.beam_energy_spreads[energy_index]
    particle_source_text = generate_particle_source_text(experiment_parameters.particle_source, beam_energy, beam_energy_spread)
    script += particle_source_text

    physics_lists_text = generate_physics_lists_text(experiment_parameters.physics_list)
    script += physics_lists_text

    scoring_text = generate_scoring_text(experiment_parameters.scorer, data_folder, beam_energy, experiment_parameters.particle_source.beam_energy_unit, number_of_histories)
    script += scoring_text

    return script

def write_script_to_file(script: List[int], script_folder_path: Path, filename: str):
    filepath = (script_folder_path / filename).resolve()
    with filepath.open("w") as f:
        for line in script:
            f.write(f"{line}\n")


def generate_scripts(experiment_parameters: ExperimentParameters):
    scripts_folder, data_folder, analysis_folder = create_file_structure(experiment_parameters.experiment_name,
                                                                         FileStructure.EXPERIMENTS.value,
                                                                         overwrite=experiment_parameters.overwrite_existing_experiment)
    beam_energies = experiment_parameters.particle_source.beam_energy
    numbers_of_histories = experiment_parameters.numbers_of_histories
    combination_of_indices = [(i, j) for i, j in product(range(len(beam_energies)), range(len(numbers_of_histories)))]
    for index_combination in combination_of_indices:
        beam_energy_index = index_combination[0]
        number_of_histories_index = index_combination[1]

        beam_energy = beam_energies[beam_energy_index]
        beam_energy_units = experiment_parameters.particle_source.beam_energy_unit
        number_of_histories = numbers_of_histories[number_of_histories_index]

        script = generate_script(experiment_parameters, beam_energy_index, number_of_histories_index, data_folder)
        filename = create_filename(beam_energy, beam_energy_units, number_of_histories)
        write_script_to_file(script, scripts_folder, filename)
    print("Scripts generation successful.")
    return 

def main():
    experiment_parameters = load_experiment_parameters()
    generate_scripts(experiment_parameters)

if __name__=="__main__":
    main()
# # Define the numbers of histories
# NUMBERS_OF_HISTORIES = [8000, 10000, 16000]
# BASE_SCRIPT_PATH = 'convergence_testing_150MeV_slices.txt'

# def main():
#     # Directory to store the generated simulation scripts and outputs
#     output_dir = 'results'
#     os.makedirs(output_dir, exist_ok=True)

#     # Read the base simulation script
#     with open(BASE_SCRIPT_PATH, 'r') as file:
#         base_script = file.read()

#     # Store results for logging
#     results = []

#     # Loop over each energy value
#     for number_of_histories in NUMBERS_OF_HISTORIES:
#         if type(number_of_histories) is not int:
#             print(f"NUMBER OF HISTORIES MUST BE AN INTEGER, not {number_of_histories} which is of type {type(number_of_histories)}.")
#             return
#         number_of_histories_string = f"{number_of_histories}"
#         unique_block_name = f"ConvergenceTesting_150MeV_Histories_{number_of_histories_string}_slices"

#         output_filename = f'output_histories_{number_of_histories}_slices.csv'
#         output_path = os.path.join(output_dir, output_filename)

#         modified_script = []
#         scoring_block_started = False

#         for line in base_script.splitlines():
#             stripped = line.strip()

#             # Replace number of histories
#             if stripped.startswith('i:So/ProtonBeam/NumberOfHistoriesInRun'):
#                 modified_script.append(f'i:So/ProtonBeam/NumberOfHistoriesInRun = {number_of_histories}')
#             # Rename the scoring block
#             elif 'Sc/ConvergenceTesting_150MeV' in stripped:
#                 new_line = line.replace('ConvergenceTesting_150MeV', unique_block_name)
#                 modified_script.append(new_line)
#                 scoring_block_started = True
#             # Add output file line directly below the scoring block header
#             elif scoring_block_started and not stripped.startswith('#') and '/OutputFile' not in stripped:
#                 modified_script.append(f's:Sc/{unique_block_name}/OutputFile = "{output_path}"')
#                 scoring_block_started = False  # Insert only once
#                 modified_script.append(line)
#             else:
#                 modified_script.append(line)

#         modified_script_content = '\n'.join(modified_script)

#         # Save the modified simulation script
#         script_filename = f'histories_{number_of_histories}_script.txt'
#         script_path = os.path.join(output_dir, script_filename)
#         with open(script_path, 'w') as f:
#             f.write(modified_script_content)

#         # Run the TOPAS simulation
#         try:
#             subprocess.run(['/home/robin/topas/bin/topas', script_path], check=True)
#             print(f"✅ Simulation for {number_of_histories} histories completed successfully.")
#             # You could parse the output here to extract Bragg peak info
#             results.append((output_path, number_of_histories_string, None, None))  # Placeholder for depth/uncertainty
#         except subprocess.CalledProcessError as e:
#             print(f"❌ Simulation for {number_of_histories} MeV failed: {e}")
#             results.append((output_path, number_of_histories_string, 'FAILED', 'FAILED'))

#     # Save paths and results to a summary file
#     with open(os.path.join(output_dir, 'summary.csv'), 'w') as f:
#         f.write('filepath,number_of_histories,bragg_peak_depth_mm,bragg_peak_uncertainty_mm\n')
#         for row in results:
#             f.write(','.join(str(x) for x in row) + '\n')

