import os
import subprocess
import json
from topas_wrapper.get_data import load_experiment_parameters, load_experiment_geometry_text

def generate_file_structure():
    return

def generate_number_of_threads_text(number_of_threads: int) -> str:
    if number_of_threads is None:
        return
    if type(number_of_threads) is not int:
        raise Exception(f"Number of threads must be an integer. You have input {number_of_threads} which is of type {type(number_of_threads)}.")
    number_of_threads_text = f"i:Ts/NumberOfThreads = {number_of_threads}"
    return number_of_threads_text


def main():
    experiment_parameters = load_experiment_parameters()
    print(experiment_parameters)
    print(experiment_parameters.numbers_of_histories)
    return

if __name__ == "__main__":
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

