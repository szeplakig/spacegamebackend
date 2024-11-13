from uuid import uuid4

from sqlmodel import Session, create_engine, select

from spacegamebackend.infra.models import UserModel
from spacegamebackend.repositories.user_repository import UserRepository
from spacegamebackend.schemas.user.user import User
from spacegamebackend.security.encrypt import salt_and_hash_password


class SqliteUserRepository(UserRepository):
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.db")

    def register_user(self, *, email: str, password: str) -> User:
        salt, hashed = salt_and_hash_password(password)
        db_user = UserModel(id=uuid4().hex, email=email, password_hash=hashed, salt=salt)
        with Session(self.engine) as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return User.model_validate(db_user)

    def login_user(self, *, email: str, password: str) -> User | None:
        with Session(self.engine) as session:
            db_user = session.exec(select(UserModel).where(UserModel.email == email)).first()
            if db_user is None:
                return None
            db_hashed = db_user.password_hash
            db_salt = db_user.salt
            _, hashed = salt_and_hash_password(password, salt_str=db_salt)
            if hashed == db_hashed:
                return User.model_validate(db_user)
            return None

    def get_user_by_id(self, *, user_id: str) -> User | None:
        with Session(self.engine) as session:
            db_user = session.exec(select(UserModel).where(UserModel.id == user_id)).first()
            return User.model_validate(db_user) if db_user else None
