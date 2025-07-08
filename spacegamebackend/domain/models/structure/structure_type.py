from enum import StrEnum, auto
from functools import lru_cache


class StructureType(StrEnum):
    # Tier 0
    MINING_FACILITY_T0 = auto()
    SOLAR_FARM_T0 = auto()
    RESEARCH_LAB_T0 = auto()
    ALLOY_FOUNDRY_T0 = auto()
    GOVERNMENT_CENTER_T0 = auto()
    OUTPOST_T0 = auto()
    MINERAL_STORAGE_T0 = auto()
    ENERGY_STORAGE_T0 = auto()
    RESEARCH_STORAGE_T0 = auto()
    ALLOY_STORAGE_T0 = auto()

    # Tier 1
    ORBITAL_SOLAR_FARM_T1 = auto()
    ORBITAL_GOVERNMENT_CENTER_T1 = auto()
    ORBITAL_MINING_FACILITY_T1 = auto()
    ORBITAL_RESEARCH_LAB_T1 = auto()
    ORBITAL_ALLOY_FOUNDRY_T1 = auto()
    DEUTERIUM_EXTRACTOR_T1 = auto()
    FUSION_REACTOR_T1 = auto()

    # Tier 2
    DEEP_SPACE_RESEARCH_LAB_T2 = auto()
    DEEP_SPACE_ALLOY_FOUNDRY_T2 = auto()
    QUANTUM_KNOWLEDGE_BASE_T2 = auto()

    # Tier 3
    ANTIMATTER_BREEDING_FACILITY_T3 = auto()
    MATTER_ANTIMATTER_REACTOR_T3 = auto()

    # Tier 4
    DARK_ENERGY_EXTRACTOR_T4 = auto()
    QUANTUM_ENERGY_REFINERY_T4 = auto()

    @staticmethod
    @lru_cache(1)
    def non_resource_generation_structures() -> set["StructureType"]:
        return {
            StructureType.MINING_FACILITY_T0,
            StructureType.SOLAR_FARM_T0,
            StructureType.RESEARCH_LAB_T0,
            StructureType.ALLOY_FOUNDRY_T0,
            StructureType.GOVERNMENT_CENTER_T0,
            StructureType.MINERAL_STORAGE_T0,
            StructureType.ENERGY_STORAGE_T0,
            StructureType.RESEARCH_STORAGE_T0,
            StructureType.ALLOY_STORAGE_T0,
            StructureType.DEUTERIUM_EXTRACTOR_T1,
            StructureType.FUSION_REACTOR_T1,
            StructureType.ORBITAL_GOVERNMENT_CENTER_T1,
        }
