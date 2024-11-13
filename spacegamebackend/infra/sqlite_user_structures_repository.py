from sqlalchemy import create_engine
from sqlmodel import Session, and_, select

from spacegamebackend.infra.models import StructuresModel
from spacegamebackend.repositories.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.schemas.structures.structure import Structure, StructureStatus
from spacegamebackend.service.handlers.get_structures_handler import StructureTemplate


class SqliteUserStructureRepository(UserStructureRepository):
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.db")

    def get_all_user_structures(self, *, user_id: str) -> list[Structure]:
        """Get all the structures of a user. If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structures = session.exec(select(StructuresModel).where(StructuresModel.user_id == user_id)).all()

        return [
            Structure(
                structure_id=db_structure.structure_id,
                entity_id=db_structure.entity_id,
                structure_type=db_structure.structure_type,
                level=db_structure.level,
                structure_status=db_structure.structure_status,
                structure_template=StructureTemplate.structure_templates[db_structure.structure_type],
            )
            for db_structure in db_structures
        ]

    def get_user_structures(self, *, user_id: str, entity_id: str) -> list[Structure]:
        """Get the structures of a user. If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structures = session.exec(
                select(StructuresModel).where(
                    and_(
                        StructuresModel.user_id == user_id,
                        StructuresModel.entity_id == entity_id,
                    )
                )
            ).all()

        return [
            Structure(
                structure_id=db_structure.structure_id,
                entity_id=db_structure.entity_id,
                structure_type=db_structure.structure_type,
                level=db_structure.level,
                structure_status=db_structure.structure_status,
                structure_template=StructureTemplate.structure_templates[db_structure.structure_type],
            )
            for db_structure in db_structures
        ]

    def add_user_structure(self, *, user_id: str, entity_id: str, structure: Structure) -> None:
        """Add a structure to the user. If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = StructuresModel(
                user_id=user_id,
                entity_id=entity_id,
                structure_id=structure.structure_id,
                level=structure.level,
                structure_type=structure.structure_type,
                structure_status=structure.structure_status,
            )
            session.add(db_structure)
            session.commit()

    def set_structure_status(self, *, structure_id: str, status: StructureStatus) -> None:
        """Set the status of a structure. If the structure does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = session.exec(
                select(StructuresModel).where(StructuresModel.structure_id == structure_id)
            ).first()
            if db_structure:
                db_structure.structure_status = status
                session.commit()
            else:
                raise Exception("Structure not found")
