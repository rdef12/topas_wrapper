from enum import Enum

class EnergyUnit(str, Enum):
    eV = "eV"
    MeV = "MeV"

class LengthUnit(str, Enum):
    cm = "cm"
    mm = "mm"

class AngleUnit(str, Enum):
    deg = "deg"
    rad = "rad"

class ParticleSourceType(str, Enum):
    Beam = "Beam"
    Isotropic = "Isotropic"
    Emittance = "Emittance"
    PhaseSpace = "PhaseSpace"

class BeamParticle(str, Enum):
    proton = "proton"

class BeamAngularDistribution(str, Enum):
    Gaussian = "Gaussian"
    Flat = "Flat"

class BeamPositionCutoffShape(str, Enum):
    Point = "Point"
    Ellipse = "Ellipse"
    Rectangle = "Rectangle"
    Isotropic = "Isotropic"

class BeamPositionDistribution(str, Enum):
    Gaussian = "Gaussian"
    Flat = "Flat"

class PhysicsList(str, Enum):
    g4h_chargeexchange = "g4h-chargeexchange"
    g4decay = "g4decay"
    g4em_dna = "g4em-dna"
    g4em_dna_opt1 = "g4em-dna_opt1"
    g4em_dna_opt2 = "g4em-dna_opt2"
    g4em_dna_opt3 = "g4em-dna_opt3"
    g4em_dna_opt4 = "g4em-dna_opt4"
    g4em_dna_opt5 = "g4em-dna_opt5"
    g4em_dna_opt6 = "g4em-dna_opt6"
    g4em_dna_opt7 = "g4em-dna_opt7"
    g4em_dna_opt8 = "g4em-dna_opt8"
    g4em_dna_stationary = "g4em-dna-stationary"
    g4em_dna_stationary_opt2 = "g4em-dna-stationary_opt2"
    g4em_dna_stationary_opt4 = "g4em-dna-stationary_opt4"
    g4em_dna_stationary_opt6 = "g4em-dna-stationary_opt6"
    g4em_dna_chemistry = "g4em-dna-chemistry"
    g4em_standard_GS = "g4em-standard_GS"
    g4em_standard_SS = "g4em-standard_SS"
    g4em_standard_WVI = "g4em-standard_WVI"
    g4h_phy_QGSP_BIC_AllHP = "g4h-phy_QGSP_BIC_AllHP"
    g4em_extra = "g4em-extra"
    g4em_livermore = "g4em-livermore"
    g4em_polarized = "g4em-polarized"
    g4em_lowep = "g4em-lowep"
    g4em_penelope = "g4em-penelope"
    g4em_standard_opt0 = "g4em-standard_opt0"
    g4em_standard_opt1 = "g4em-standard_opt1"
    g4em_standard_opt2 = "g4em-standard_opt2"
    g4em_standard_opt3 = "g4em-standard_opt3"
    g4em_standard_opt4 = "g4em-standard_opt4"
    g4h_elastic_D = "g4h-elastic_D"
    g4h_elastic = "g4h-elastic"
    g4h_elastic_HP = "g4h-elastic_HP"
    g4h_elastic_LEND = "g4h-elastic_LEND"
    g4h_elastic_XS = "g4h-elastic_XS"
    g4h_elastic_H = "g4h-elastic_H"
    g4h_inelastic_QBBC = "g4h-inelastic_QBBC"
    g4h_phy_FTFP_BERT = "g4h-phy_FTFP_BERT"
    g4h_phy_FTFP_BERT_HP = "g4h-phy_FTFP_BERT_HP"
    g4h_phy_FTFP_BERT_TRV = "g4h-phy_FTFP_BERT_TRV"
    g4h_phy_FTF_BIC = "g4h-phy_FTF_BIC"
    g4h_phy_QGSP_BERT = "g4h-phy_QGSP_BERT"
    g4h_phy_QGSP_BERT_HP = "g4h-phy_QGSP_BERT_HP"
    g4h_phy_QGSP_BIC = "g4h-phy_QGSP_BIC"
    g4h_phy_QGSP_BIC_HP = "g4h-phy_QGSP_BIC_HP"
    g4h_phy_QGSP_FTFP_BERT = "g4h-phy_QGSP_FTFP_BERT"
    g4h_phy_QGS_BIC = "g4h-phy_QGS_BIC"
    g4h_phy_Shielding = "g4h-phy_Shielding"
    g4ion_binarycascade = "g4ion-binarycascade"
    g4ion_inclxx = "g4ion-inclxx"
    g4ion = "g4ion"
    g4ion_QMD = "g4ion-QMD"
    g4n_trackingcut = "g4n-trackingcut"
    g4optical = "g4optical"
    g4radioactivedecay = "g4radioactivedecay"
    g4stopping = "g4stopping"

class PhysicsListType(str, Enum):
    Geant4_Modular = "Geant4_Modular"


class ScorerQuantity(str, Enum):
    DoseToMedium = "DoseToMedium"
    DoseToWater = "DoseToWater"
    DoseToMaterial = "DoseToMaterial"
    TrackLengthEstimator = "TrackLengthEstimator"
    AmbientDoseEquivalent = "AmbientDoseEquivalent"
    EnergyDeposit = "EnergyDeposit"
    Fluence = "Fluence"
    EnergyFluence = "EnergyFluence"
    StepCount = "StepCount"
    OpticalPhotonCount = "OpticalPhotonCount"
    OriginCount = "OriginCount"
    Charge = "Charge"
    EffectiveCharge = "EffectiveCharge"
    ProtonLET = "ProtonLET"

class ParticleType(str, Enum): #PDG codes not currently supported
    proton = "proton"
    neutron = "neutron"
    e_p = "e+"
    e_m = "e-"
    gamma = "gamma"
    He3 = "He3"
    alpha = "alpha"
    deuteron = "deuteron"
    triton = "triton"
    opticalphoton = "opticalphoton"
    geantino = "geantino"
    chargedgeantino = "chargedgeantino"