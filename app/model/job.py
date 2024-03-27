from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    Date,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import JobStatus, Gender, JobType, SalaryType


class Job(Base):
    company_id = Column(
        Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    representative_id = Column(Integer, ForeignKey("representative.id"), nullable=False)
    job_experience_id = Column(Integer, ForeignKey("job_experience.id"), nullable=False)
    working_time_id = Column(Integer, ForeignKey("working_time.id"), nullable=False)
    job_main_category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    job_position_id = Column(Integer, ForeignKey("job_position.id"), nullable=False)
    title = Column(String(255), index=True, nullable=False)
    job_description = Column(String(500), nullable=False)
    job_requirement = Column(String(500), nullable=False)
    job_benefit = Column(String(500), nullable=False)
    job_location = Column(String(255), nullable=False)
    max_salary = Column(Integer, default=0, nullable=True)
    min_salary = Column(Integer, default=0, nullable=True)
    salary_type = Column(
        Enum(SalaryType), default=SalaryType.VND, nullable=False, index=True
    )
    full_name_contact = Column(String(50), nullable=False)
    phone_number_contact = Column(String(10), nullable=False)
    email_contact = Column(String(50), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    employment_type = Column(Enum(JobType), default=JobType.FULL_TIME)
    gender_requirement = Column(Enum(Gender), default=Gender.OTHER)
    deadline = Column(Date, nullable=False)
    employer_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    is_highlight = Column(Boolean, default=False)
    is_urgent = Column(Boolean, default=False)
    is_paid_featured = Column(Boolean, default=False)
    is_bg_featured = Column(Boolean, default=False)
    is_vip_employer = Column(Boolean, default=False)
    is_diamond_employer = Column(Boolean, default=False)
    is_job_flash = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="job", uselist=False)
    representative = relationship("Representative", back_populates="job", uselist=False)
    job_experience = relationship("JobExperience", back_populates="job", uselist=False)
    cv_application = relationship("CVApplication", back_populates="job")
    job_approval_request = relationship("JobApprovalRequest", back_populates="job")
    skill = relationship("Skill", secondary="job_skill")
    job_sub_category = relationship("Category", secondary="job_sub_category")
    job_position = relationship("JobPosition", back_populates="job")
    job_report = relationship("JobReport", back_populates="job")
    user_job_save = relationship("UserJobSave", back_populates="job")
    working_time = relationship("WorkingTime", secondary="job_working_time")
