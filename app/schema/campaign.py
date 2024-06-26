from pydantic import BaseModel, validator, ConfigDict
from typing import Optional
from datetime import datetime

from app.hepler.enum import CampaignStatus
from app.schema.page import Pagination


class CampaignBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attribute=True)

    title: str
    is_flash: Optional[bool] = False

    @validator("title")
    def validate_title(cls, v):
        if len(v) < 1 or len(v) > 255:
            raise ValueError("Invalid title")
        return v


class CampaignItemResponse(CampaignBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: Optional[CampaignStatus] = CampaignStatus.OPEN
    optimal_score: Optional[int] = 0
    job: Optional[dict] = None

    @validator("status")
    def validate_status(cls, v):
        return v or CampaignStatus.OPEN

    @validator("optimal_score")
    def validate_optimal_score(cls, v):
        return v or 0


class CampaignGetRequest(BaseModel):
    id: int


class CampaignGetByBusinessIdRequest(BaseModel):
    business_id: int


class CampaignCreateRequest(CampaignBase):
    pass


class CampaignCreate(CampaignBase):
    business_id: int


class CampaignUpdateRequest(CampaignBase):
    status: Optional[str] = CampaignStatus.OPEN
    optimal_score: Optional[int] = 0
    id: int

    @validator("status")
    def validate_status(cls, v):
        if not v in CampaignStatus.__members__.values():
            raise ValueError("Invalid status")
        return v or CampaignStatus.OPEN

    @validator("optimal_score")
    def validate_optimal_score(cls, v):
        return v or 0


class CampaignUpdate(CampaignBase):
    status: Optional[str] = CampaignStatus.OPEN
    optimal_score: Optional[int] = 0
    id: int

    @validator("status")
    def validate_status(cls, v):
        if not v in CampaignStatus.__members__.values():
            raise ValueError("Invalid status")
        return v or CampaignStatus.OPEN

    @validator("optimal_score")
    def validate_optimal_score(cls, v):
        return v or 0


class CampaignDeleteRequest(BaseModel):
    id: int


class CampaignGetListPagination(Pagination):
    business_id: Optional[int] = None
    company_id: Optional[int] = None
    status: Optional[CampaignStatus] = None

    @validator("status")
    def validate_status(cls, v):
        if v and not v in CampaignStatus.__members__.values():
            raise ValueError("Invalid status")
        return v


class CountGetListPagination(BaseModel):
    business_id: Optional[int] = None
    company_id: Optional[int] = None
    status: Optional[CampaignStatus] = None
