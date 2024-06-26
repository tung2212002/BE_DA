from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_password_hash, verify_password
from .base import CRUDBase
from app.model.manager_base import ManagerBase
from app.schema import manager_base as schema_manager_base
from app.hepler.enum import Role


class CRUDManagerBase(
    CRUDBase[
        ManagerBase,
        schema_manager_base.ManagerBaseCreateRequest,
        schema_manager_base.ManagerBaseUpdateRequest,
    ]
):

    def get(self, db: Session, id: int) -> ManagerBase:
        return (
            db.query(self.model)
            .filter(self.model.id == id, self.model.role == Role.BUSINESS)
            .first()
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[ManagerBase]:
        return (
            db.query(self.model)
            .filter(self.model.role == Role.BUSINESS)
            .order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_admin(self, db: Session, id: int) -> ManagerBase:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi_by_admin(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[ManagerBase]:
        return (
            db.query(self.model)
            .order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_list_admin(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[ManagerBase]:
        return (
            db.query(self.model)
            .filter(self.model.role == Role.ADMIN)
            .order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_list_business(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order_by: str = "desc",
    ) -> List[ManagerBase]:

        return (
            db.query(self.model)
            .filter(self.model.role == Role.BUSINESS)
            .order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_email(self, db: Session, email: str) -> ManagerBase:
        return db.query(ManagerBase).filter(ManagerBase.email == email).first()

    def create(
        self, db: Session, *, obj_in: schema_manager_base.ManagerBaseCreate
    ) -> ManagerBase:
        db_obj = ManagerBase(
            **obj_in.model_dump(
                exclude_unset=True, exclude={"password", "confirm_password"}
            ),
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ManagerBase,
        obj_in: schema_manager_base.ManagerBaseUpdateRequest,
    ) -> ManagerBase:

        if isinstance(obj_in, dict):
            if obj_in.get("password"):
                obj_in["hashed_password"] = get_password_hash(obj_in["password"])
                obj_in.pop("password")
        elif hasattr(obj_in, "password") and obj_in.password:
            obj_in = obj_in.copy(
                update={"hashed_password": get_password_hash(obj_in.password)}
            )
            obj_in.pop("password")
            obj_in.pop("confirm_password")
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> ManagerBase:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: ManagerBase) -> bool:
        return user.is_active

    def is_superuser(self, user: ManagerBase) -> bool:
        return user.role == Role.SUPER_USER

    def set_active(
        self, db: Session, *, db_obj: ManagerBase, is_active: bool
    ) -> ManagerBase:
        db_obj.is_active = is_active
        db.commit()
        db.refresh(db_obj)
        return db_obj


manager_base = CRUDManagerBase(ManagerBase)
