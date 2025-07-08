from sqlalchemy import create_engine
from sqlmodel import Session, and_, func, select

from spacegamebackend.domain.models.structure.structure import Structure
from spacegamebackend.domain.models.structure.structure_status import StructureStatus
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.infra.models.structure.structure_model import StructuresModel


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
                structure_type=StructureType(db_structure.structure_type),
                level=db_structure.level,
                structure_status=db_structure.structure_status,
                structure_template=StructureTemplate.get_structure_template(StructureType(db_structure.structure_type)),
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
                structure_type=StructureType(db_structure.structure_type),
                level=db_structure.level,
                structure_status=db_structure.structure_status,
                structure_template=StructureTemplate.get_structure_template(StructureType(db_structure.structure_type)),
            )
            for db_structure in db_structures
        ]

    def get_user_structures_at(self, *, user_id: str, x: int, y: int) -> list[Structure]:
        """Get the structures of a user at a specific position. If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structures = session.exec(
                select(StructuresModel).where(
                    and_(
                        StructuresModel.user_id == user_id,
                        StructuresModel.x == x,
                        StructuresModel.y == y,
                    )
                )
            ).all()
        return [
            Structure(
                structure_id=db_structure.structure_id,
                entity_id=db_structure.entity_id,
                structure_type=StructureType(db_structure.structure_type),
                level=db_structure.level,
                structure_status=db_structure.structure_status,
                structure_template=StructureTemplate.get_structure_template(StructureType(db_structure.structure_type)),
            )
            for db_structure in db_structures
        ]

    def has_structure(self, *, user_id: str, entity_id: str, structure_type: StructureType) -> bool:
        """Check if a user has a structure. If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = session.exec(
                select(StructuresModel).where(
                    and_(
                        StructuresModel.user_id == user_id,
                        StructuresModel.entity_id == entity_id,
                        StructuresModel.structure_type == structure_type.value,
                    )
                )
            ).first()
        return db_structure is not None

    def has_structure_at(self, *, user_id: str, x: int, y: int, structure_type: StructureType) -> bool:
        """Check if a user has a structure at a specific position. If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = session.exec(
                select(StructuresModel).where(
                    and_(
                        StructuresModel.user_id == user_id,
                        StructuresModel.x == x,
                        StructuresModel.y == y,
                        StructuresModel.structure_type == structure_type.value,
                    )
                )
            ).first()
        return db_structure is not None

    def get_structure(self, *, structure_id: str) -> Structure:
        """Get a structure. If the structure does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = session.exec(
                select(StructuresModel).where(StructuresModel.structure_id == structure_id)
            ).first()

        if db_structure:
            return Structure(
                structure_id=db_structure.structure_id,
                entity_id=db_structure.entity_id,
                structure_type=StructureType(db_structure.structure_type),
                level=db_structure.level,
                structure_status=db_structure.structure_status,
                structure_template=StructureTemplate.get_structure_template(StructureType(db_structure.structure_type)),
            )
        raise Exception("Structure not found")

    def add_user_structure(self, *, user_id: str, entity_id: str, x: int, y: int, structure: Structure) -> None:
        """Add a structure to the user. If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = StructuresModel(
                user_id=user_id,
                entity_id=entity_id,
                x=x,
                y=y,
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

    def upgrade_structure(self, *, structure_id: str) -> None:
        """Upgrade a structure. If the structure does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = session.exec(
                select(StructuresModel).where(StructuresModel.structure_id == structure_id)
            ).first()
            if db_structure:
                db_structure.level += 1
                session.commit()
            else:
                raise Exception("Structure not found")

    def delete_user_structure(self, *, structure_id: str) -> None:
        """Delete a structure. If the structure does not exist, raise an exception."""
        with Session(self.engine) as session:
            db_structure = session.exec(
                select(StructuresModel).where(StructuresModel.structure_id == structure_id)
            ).first()
            if db_structure:
                session.delete(db_structure)
                session.commit()
            else:
                raise Exception("Structure not found")

    def get_user_structure_levels(self, *, user_id: str, entity_id: str | None = None) -> dict[StructureType, int]:
        """Get the max levels of structures for a user, optionally filtered by entity.
        This method returns a dictionary where the keys are StructureType and the values are the maximum levels.
        If the user does not exist, raise an exception."""
        with Session(self.engine) as session:
            query = select(StructuresModel.structure_type, func.max(StructuresModel.level)).where(  # type: ignore[var-annotated]
                StructuresModel.user_id == user_id
            )
            if entity_id is not None:
                query = query.where(StructuresModel.entity_id == entity_id)
            query = query.group_by(StructuresModel.structure_type)
            results = session.exec(query).all()
            return {StructureType(result[0]): result[1] for result in results} if results else {}
