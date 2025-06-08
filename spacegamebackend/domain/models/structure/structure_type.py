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
    STARTER_OUTPOST = auto()

    # Tier 1
    ORBITAL_SOLAR_FARM = auto()
    DEEP_SPACE_RESEARCH_STATION = auto()
    MEGA_DEEP_SPACE_PARTICLE_ACCELERATOR = auto()
    DARK_MATTER_ENGINE = auto()

    @staticmethod
    @lru_cache(1)
    def tier_0() -> set["StructureType"]:
        return {
            StructureType.MINING_FACILITY,
            StructureType.SOLAR_FARM,
            StructureType.RESEARCH_LAB,
            StructureType.ALLOY_FOUNDRY,
            StructureType.GOVERNMENT_CENTER,
            StructureType.DEUTERIUM_EXTRACTOR,
            StructureType.FUSION_REACTOR,
            StructureType.OUTPOST,
        }

    @staticmethod
    @lru_cache(1)
    def tier_1() -> set["StructureType"]:
        return {
            StructureType.ORBITAL_SOLAR_FARM,
            StructureType.DEEP_SPACE_RESEARCH_STATION,
            StructureType.MEGA_DEEP_SPACE_PARTICLE_ACCELERATOR,
            StructureType.DARK_MATTER_ENGINE,
        }
