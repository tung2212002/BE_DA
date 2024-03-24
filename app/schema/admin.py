from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional

from app.hepler.enum import Role, Gender
from app.core import constant


class AdminBase(BaseModel):
    full_name: str = Field(
        ...,
    )
    email: str = Field(
        ...,
    )
    gender: Gender
    phone_number: str

    model_config = ConfigDict(from_attribute=True)

    @validator("full_name")
    def validate_full_name(cls, v):
        if len(v) < 3:
            raise ValueError("Full name must be at least 3 characters")
        elif len(v) > 50:
            raise ValueError("Full name must be at most 50 characters")
        elif not v.replace(" ", "").isalpha():
            raise ValueError("Full name must be alphabet")
        return v

    @validator("email")
    def validate_email(cls, v):
        if not re.fullmatch(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v

    @validator("gender")
    def validate_gender(cls, v):
        if v not in Gender.__members__.values():
            raise ValueError("Invalid gender")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(constant.REGEX_PHONE_NUMBER, v):
            raise ValueError("Invalid phone number")
        return v


class AdminItemResponse(AdminBase):
    id: int
    avatar: Optional[str] = None
    is_active: bool
    role: Role


class UserGetRequest(BaseModel):
    email: str = Field(..., example="1@email.com")

    @validator("email")
    def validate_email(cls, v):
        if not re.fullmatch(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
        return v


class AdminCreateRequest(AdminBase):
    avatar: Optional[UploadFile] = None
    password: str
    confirm_password: str
    role: Role = Role.ADMIN

    @validator("password")
    def validate_password(cls, v, values):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif len(v) > 50:
            raise ValueError("Password must be at most 50 characters")
        elif not re.match(constant.REGEX_PASSWORD, v):
            raise ValueError(
                "Password must contain at least one special character, one digit, one alphabet, one uppercase letter"
            )
        elif "confirm_password" in values and v != values["confirm_password"]:
            raise ValueError("Password and confirm password must match")
        return v

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
        return v


class AdminUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    avatar: Optional[UploadFile] = None
    gender: Optional[Gender] = None

    @validator("full_name")
    def validate_full_name(cls, v):
        if v is not None:
            if len(v) < 3:
                raise ValueError("Full name must be at least 3 characters")
            elif len(v) > 50:
                raise ValueError("Full name must be at most 50 characters")
            elif not v.replace(" ", "").isalpha():
                raise ValueError("Full name must be alphabet")
            return v

    @validator("email")
    def validate_email(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_EMAIL, v):
                raise ValueError("Invalid email")
            return v

    @validator("avatar")
    def validate_avatar(cls, v):
        if v is not None:
            if v.content_type not in constant.ALLOWED_IMAGE_TYPES:
                raise ValueError("Invalid image type")
            elif v.size > constant.MAX_IMAGE_SIZE:
                raise ValueError("Image size must be at most 2MB")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None:
            if not re.match(constant.REGEX_PHONE_NUMBER, v):
                raise ValueError("Invalid phone number")

    @validator("gender")
    def validate_gender(cls, v):
        if v is not None:
            if v not in Gender.__members__.values():
                raise ValueError("Invalid gender")
            return v