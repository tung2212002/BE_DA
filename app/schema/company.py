from pydantic import BaseModel, validator, ConfigDict
import re
from fastapi import UploadFile
from typing import Optional, List, Any
import json


from app.hepler.enum import CompanyType, FolderBucket
from app.core import constant
from app.hepler.generate_file_name import generate_file_name
from app.schema.page import Pagination


class CompanyBase(BaseModel):
    name: str
    email: str
    phone_number: str
    is_premium: bool = False
    website: Optional[str] = None
    address: str
    company_short_description: Optional[str] = None
    scale: str
    tax_code: str
    type: CompanyType

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("name")
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("Name must be at least 3 characters")
        elif len(v) > 255:
            raise ValueError("Name must be at most 255 characters")
        return v

    @validator("email")
    def validate_email(cls, v):
        if not re.fullmatch(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(constant.REGEX_PHONE_NUMBER, v):
            raise ValueError("Invalid phone number")
        return v


class CompanyItemResponse(BaseModel):
    id: int
    name: str
    email: str
    type: CompanyType
    phone_number: str
    is_premium: bool
    label: Optional[object] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    address: str
    company_short_description: Optional[str] = None
    scale: str
    is_verified: bool
    total_active_jobs: int = None
    tax_code: str
    banner: Optional[str] = None

    @validator("logo")
    def validate_logo(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v

    @validator("company_short_description")
    def validate_company_short_description(cls, v):
        if v is not None:
            return json.loads(v) if isinstance(v, str) else v

    @validator("banner")
    def validate_banner(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v


class CompanyPrivateResponse(BaseModel):
    id: int
    name: str
    email: str
    type: CompanyType
    phone_number: str
    is_premium: bool
    label: Optional[object] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    address: str
    company_short_description: Optional[str] = None
    scale: str
    tax_code: str
    is_verified: bool
    total_active_jobs: int = 0
    banner: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("logo")
    def validate_logo(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v

    @validator("company_short_description")
    def validate_company_short_description(cls, v):
        if v is not None:
            return json.loads(v) if isinstance(v, str) else v

    @validator("banner")
    def validate_banner(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v


class CompanyJobResponse(CompanyBase):
    id: int
    name: str
    logo: Optional[str] = None

    @validator("logo")
    def validate_logo(cls, v):
        if v is not None:
            if not v.startswith("https://"):
                v = constant.BUCKET_URL + v
        return v

    @validator("company_short_description")
    def validate_company_short_description(cls, v):
        if v is not None:
            return json.loads(v) if isinstance(v, str) else v


class CompanyGetRequest(BaseModel):
    id: int


class CompanyPagination(Pagination):
    fields: Optional[List[int]] = None
    business_id: Optional[int] = None
    keyword: Optional[str] = None


class CompanyCreateRequest(CompanyBase):
    fields: List
    logo: Optional[UploadFile] = None

    @validator("logo")
    def validate_logo(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
            v.filename = generate_file_name(FolderBucket.LOGO, v.filename)
        return v

    @validator("company_short_description")
    def validate_company_short_description(cls, v):
        if v is not None:
            return json.dumps(v)
        return v

    @validator("fields")
    def validate_fields(cls, v):
        if len(v) == 0:
            raise ValueError("Fields must not be empty")
        return v


class CompanyCreate(CompanyBase):
    logo: Optional[str] = None
    business_id: int


class CompanyUpdateRequest(BaseModel):
    company_id: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    is_premium: Optional[bool] = None
    label: Optional[str] = None
    logo: Optional[UploadFile] = None
    website: Optional[str] = None
    address: Optional[str] = None
    type: Optional[CompanyType] = None
    company_short_description: Optional[str] = None
    scale: Optional[str] = None
    tax_code: Optional[str] = None
    fields: Optional[List] = None

    @validator("email")
    def validate_email(cls, v):
        if v is not None:
            if not re.fullmatch(constant.REGEX_EMAIL, v):
                raise ValueError("Invalid email")
            return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")
            return v

    @validator("logo")
    def validate_logo(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
            v.filename = generate_file_name(FolderBucket.LOGO, v.filename)
        return v

    @validator("company_short_description")
    def validate_company_short_description(cls, v):
        if v is not None:
            return json.dumps(v)
        return v


class CompanyUpdate(BaseModel):
    company_id: int
    email: Optional[str] = None
    phone_number: Optional[str] = None
    is_premium: Optional[bool] = None
    label: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    type: Optional[CompanyType] = None
    company_short_description: Optional[str] = None
    scale: Optional[str] = None
    tax_code: Optional[str] = None
    business_id: Optional[int] = None

    @validator("email")
    def validate_email(cls, v):
        if v is not None:
            if not re.fullmatch(constant.REGEX_EMAIL, v):
                raise ValueError("Invalid email")
            return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")
            return v
