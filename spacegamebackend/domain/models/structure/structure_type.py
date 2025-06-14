from enum import StrEnum, auto
from functools import lru_cache


class StructureType(StrEnum):
    # Tier 0
    MINING_FACILITY = auto()
    SOLAR_FARM = auto()
    RESEARCH_LAB = auto()
    ALLOY_FOUNDRY = auto()
    GOVERNMENT_CENTER = auto()
    ORBITAL_GOVERNMENT_CENTER = auto()
    DEUTERIUM_EXTRACTOR = auto()
    FUSION_REACTOR = auto()
    OUTPOST = auto()
    MINERAL_STORAGE = auto()
    ENERGY_STORAGE = auto()

    # Tier 1
    ORBITAL_SOLAR_FARM = auto()

    @staticmethod
    @lru_cache(1)
    def non_unique() -> set["StructureType"]:
        return {
            StructureType.MINING_FACILITY,
            StructureType.SOLAR_FARM,
            StructureType.RESEARCH_LAB,
            StructureType.ALLOY_FOUNDRY,
            StructureType.GOVERNMENT_CENTER,
            StructureType.ORBITAL_GOVERNMENT_CENTER,
            StructureType.DEUTERIUM_EXTRACTOR,
            StructureType.FUSION_REACTOR,
            StructureType.MINERAL_STORAGE,
            StructureType.ENERGY_STORAGE,
        }
