from sqlalchemy.orm import Session


from .base import CRUDBase
from app.model import WorkLocation
from app.schema.work_location import WorkLocatioCreate, WorkLocatioUpdate


class CRUDWorkLocation(CRUDBase[WorkLocation, WorkLocatioCreate, WorkLocatioUpdate]):
    def get_work_locations_by_job_id(self, db: Session, job_id: int):
        work_locations = db.query(self.model).filter(self.model.job_id == job_id).all()
        return work_locations


work_location = CRUDWorkLocation(WorkLocation)
