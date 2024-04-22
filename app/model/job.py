from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    Date,
    JSON,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import JobStatus, Gender, JobType, SalaryType


class Job(Base):
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    job_experience_id = Column(Integer, ForeignKey("job_experience.id"), nullable=False)
    job_position_id = Column(Integer, nullable=False)
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
    quantity = Column(Integer, default=1, nullable=False)
    full_name_contact = Column(String(50), nullable=False)
    phone_number_contact = Column(String(10), nullable=False)
    email_contact = Column(JSON, nullable=False)
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
    working_time_text = Column(String(255), nullable=True)
    campaign_id = Column(
        Integer,
        ForeignKey("campaign.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    business = relationship("Business", back_populates="job", uselist=False)
    job_experience = relationship("JobExperience", back_populates="job", uselist=False)
    cv_applications = relationship("CVApplication", back_populates="job")
    job_approval_request = relationship("JobApprovalRequest", back_populates="job")
    must_have_skills = relationship(
        "Skill", secondary="job_skill", overlaps="should_have_skills"
    )
    should_have_skills = relationship(
        "Skill", secondary="job_skill", overlaps="must_have_skills"
    )
    job_categories = relationship("Category", secondary="job_category")
    job_reports = relationship("JobReport", back_populates="job")
    user_job_save = relationship("UserJobSave", back_populates="job")
    working_times = relationship("WorkingTime", back_populates="job")
    campaign = relationship("Campaign", back_populates="job")
    work_locations = relationship("WorkLocation", back_populates="job", uselist=True)

    job_category_secondary = relationship(
        "JobCategory", back_populates="job", uselist=True, overlaps="job_categories"
    )
    job_skill_secondary = relationship(
        "JobSkill",
        back_populates="job",
        uselist=True,
        overlaps="must_have_skills,should_have_skills",
    )
