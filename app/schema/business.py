from pydantic import BaseModel, validator, ConfigDict
import re
from fastapi import UploadFile
from typing import Optional, Any
from datetime import datetime

from app.hepler.enum import Role, Gender, FolderBucket
from app.core import constant
from app.hepler.generate_file_name import generate_file_name


class BusinessBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attribute=True)

    phone_number: str
    gender: str
    company_name: str
    work_position: str
    work_location: Optional[str] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(constant.REGEX_PHONE_NUMBER, v):
            raise ValueError("Invalid phone number")
        return v

    @validator("gender")
    def validate_gender(cls, v):
        if not v in Gender.__members__.values():
            raise ValueError("Invalid gender")
        return v


class BusinessItemResponse(BusinessBase):

    id: int
    full_name: str
    email: str
    avatar: Optional[str] = None
    is_active: bool
    role: Role
    work_location: Optional[str] = None
    work_position: str
    updated_at: str
    created_at: str
    province: Optional[dict] = None
    district: Optional[dict] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_verified_email: bool
    is_verified_phone: bool
    is_verified_company: bool
    is_verified_identity: bool

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v


class BusinessGetRequest(BaseModel):
    id: int


class BusinessGetByEmailRequest(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        if not re.match(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v


class BusinessCreateRequest(BusinessBase):
    province_id: int
    district_id: Optional[int] = None


class BusinessCreate(BusinessCreateRequest):
    pass


class BusinessUpdateRequest(BaseModel):
    phone_number: Optional[str] = None
    gender: Optional[Gender] = None
    company_name: Optional[str] = None
    work_position: Optional[str] = None
    work_location: Optional[str] = None
    province_id: Optional[int] = None
    district_id: Optional[int] = None
    avatar: Optional[UploadFile] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")
            return v

    @validator("gender")
    def validate_gender(cls, v):
        if v is not None:
            if v not in Gender.__members__.values():
                raise ValueError("Invalid gender")
            return v

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
            v.filename = generate_file_name(FolderBucket.AVATAR, v.filename)
        return v


class BusinessUpdate(BusinessUpdateRequest):
    pass
