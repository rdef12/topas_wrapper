from pathlib import Path
from typing import List, Type
from dataclasses import dataclass
from pydantic import BaseModel, model_validator, ValidationError
import tomli

from topas_wrapper.input_constants import (EnergyUnit,
                                           LengthUnit,
                                           AngleUnit,
                                           ParticleSourceType,
                                           BeamParticle,
                                           BeamAngularDistribution,
                                           BeamPositionCutoffShape,
                                           BeamPositionDistribution,
                                           PhysicsList,
                                           PhysicsListType,
                                           ScorerQuantity,
                                           ParticleType)

RELATIVE_EXPERIMENT_GEOMETRY_PATH = "../../EXPERIMENT_GEOMETRY.txt"
RELATIVE_EXPERIMENT_PARAMETER_PATH = "../../EXPERIMENT_PARAMETERS.toml"

@dataclass
class ParticleSource(BaseModel):
    component: str #Input to match geometry source

    type: ParticleSourceType    
    beam_particle: BeamParticle
    beam_energy: List[float]
    beam_energy_unit: EnergyUnit
    beam_energy_spreads: List[float]
    beam_position_distribution: BeamPositionDistribution
    beam_position_cutoff_shape: BeamPositionCutoffShape
    beam_position_cutoff_x: float
    beam_position_cutoff_x_units: LengthUnit
    beam_position_cutoff_y: float
    beam_position_cutoff_y_units: LengthUnit
    beam_position_spread_x: float
    beam_position_spread_x_units: LengthUnit
    beam_position_spread_y: float
    beam_position_spread_y_units: LengthUnit
    beam_angular_distribution: BeamAngularDistribution
    beam_angular_cutoff_x: float
    beam_angular_cutoff_x_units: AngleUnit
    beam_angular_cutoff_y: float
    beam_angular_cutoff_y_units: AngleUnit
    beam_angular_spread_x: float
    beam_angular_spread_x_units: AngleUnit
    beam_angular_spread_y: float
    beam_angular_spread_y_units: AngleUnit

    @model_validator(mode="before")
    def check_energy_lengths(cls, values):
        energies = values.get('beam_energy')
        spreads = values.get('beam_energy_spreads')
        number_of_energy_entries = len(energies)
        number_of_spread_entries = len(spreads)
        if number_of_energy_entries != number_of_spread_entries:
            if number_of_spread_entries == 1:
                new_spreads = spreads * number_of_energy_entries
                values['beam_energy_spreads'] = new_spreads
            else:
                raise ValueError(f"beam_energy_spread must have the same number of entries as beam_energies or have only one entry.\
                                 \nThe inputted entries are beam_energies: {energies} and beam_energy_spreads {spreads}.")
        return values

@dataclass
class ExperimentPhysicsList(BaseModel):
    list_name: str
    list_processes: bool
    type: PhysicsListType
    modules: List[PhysicsList]
    EM_range_min: float
    EM_range_min_units: EnergyUnit 
    EM_range_max: float
    EM_range_max_units: EnergyUnit 

@dataclass
class Scorer(BaseModel):
    quantity: ScorerQuantity
    component: str #As named in geometry
    only_include_particles_named: ParticleType | None
    x_bins: int | None
    y_bins: int | None
    z_bins: int | None

@dataclass
class ExperimentParameters(BaseModel):
    experiment_name: str
    overwrite_existing_experiment: bool

    number_of_threads: int
    numbers_of_histories: List[int]

    particle_source: ParticleSource
    physics_list: ExperimentPhysicsList

    @classmethod
    def from_json(cls, filepath: Path):
        json_string = Path(filepath).read_text()
        return cls.model_validate_json(json_string)
    
    @classmethod
    def from_toml(cls, filepath: Path):
        with open(filepath, 'rb') as f:
            data = tomli.load(f)
            return cls.model_validate(data)


def locate_experiment_file(relative_filepath: str) -> Path:
    mod_path = Path(__file__).parent
    absolute_path = (mod_path / relative_filepath).resolve()
    if not absolute_path.exists():
        raise FileNotFoundError(f"No file exists at location -> {absolute_path}.")
    return absolute_path


def load_experiment_geometry_text() -> List[str]:
    try:
        experiment_geometry_path = locate_experiment_file(RELATIVE_EXPERIMENT_GEOMETRY_PATH)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"EXPERIMENT_GEOMETRY.txt does not exist in the expected location. \n{e} \nRefer to the original file structure.")
    geometry_lines = experiment_geometry_path.read_text().splitlines()    
    return geometry_lines


def load_experiment_parameters() -> ExperimentParameters:
    try:
        experiment_parameters_path = locate_experiment_file(RELATIVE_EXPERIMENT_PARAMETER_PATH)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"EXPERIMENT_PARAMETER.txt does not exist in the expected location. \n{e} \nRefer to the original file structure.")
    experiment_parameters = ExperimentParameters.from_toml(experiment_parameters_path)
    return experiment_parameters