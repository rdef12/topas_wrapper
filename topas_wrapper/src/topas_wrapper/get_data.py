from pathlib import Path
from typing import List, Type, Optional
from dataclasses import dataclass
from pydantic import BaseModel, model_validator, ValidationError, Field, field_validator
import tomli
from topas_wrapper.file_structure import FileStructure

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

@dataclass
class ParticleSource(BaseModel): #TODO Add limits on values of energy etc
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
    
    @field_validator("beam_energy", "beam_energy_spreads")
    def all_non_negative(cls, values):
        if any(i < 0 for i in values):
            raise ValueError("All beam energies and spreads must be zero or greater")
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
    x_bins: Optional[int] = Field(None, gt=0)
    y_bins: Optional[int] = Field(None, gt=0)
    z_bins: Optional[int] = Field(None, gt=0)

@dataclass
class ExperimentParameters(BaseModel):
    experiment_name: str
    overwrite_existing_experiment: bool

    number_of_threads: int = Field(..., ge=0)
    seed_number: int = Field(..., ge=0)
    numbers_of_histories: List[int]

    particle_source: ParticleSource
    physics_list: ExperimentPhysicsList
    scorer: Scorer

    @classmethod
    def from_json(cls, filepath: Path):
        json_string = Path(filepath).read_text()
        return cls.model_validate_json(json_string)
    
    @classmethod
    def from_toml(cls, filepath: Path):
        with open(filepath, 'rb') as f:
            data = tomli.load(f)
            return cls.model_validate(data)
    
    @field_validator("numbers_of_histories")
    def all_non_negative(cls, values):
        if any(i < 0 for i in values):
            raise ValueError("All numbers of histories must be zero or greater")
        return values


def locate_experiment_config_file(relative_filepath: str) -> Path:
    mod_path = Path(__file__).parent
    absolute_path = (mod_path / relative_filepath).resolve()
    if not absolute_path.exists():
        raise FileNotFoundError(f"No file exists at location -> {absolute_path}.")
    return absolute_path


def load_experiment_geometry_text() -> List[str]:
    try:
        experiment_geometry_path = locate_experiment_config_file(FileStructure.GEOMETRY.value)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"EXPERIMENT_GEOMETRY.txt does not exist in the expected location. \n{e} \nRefer to the original file structure.")
    geometry_lines = experiment_geometry_path.read_text().splitlines()    
    return geometry_lines


def load_experiment_parameters() -> ExperimentParameters:
    try:
        experiment_parameters_path = locate_experiment_config_file(FileStructure.PARAMETERS.value)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"EXPERIMENT_PARAMETER.txt does not exist in the expected location. \n{e} \nRefer to the original file structure.")
    experiment_parameters = ExperimentParameters.from_toml(experiment_parameters_path)
    return experiment_parameters