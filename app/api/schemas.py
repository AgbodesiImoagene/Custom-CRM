from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from app.db.models import (
    StatusEnum,
    StageEnum,
    IndustryEnum,
    LeadStatusEnum,
    RoleEnum,
)


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    username: str
    role: RoleEnum


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.user
    disabled: bool = False


class UserUpdate(UserBase):
    password: Optional[str] = None
    disabled: Optional[bool] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    role: RoleEnum
    disabled: bool

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class DomainBase(BaseModel):
    name: str
    company_id: Optional[int]


class DomainCreate(DomainBase):
    pass


class DomainUpdate(DomainBase):
    pass


class Domain(DomainBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class CompanyBase(BaseModel):
    name: str
    industry: IndustryEnum
    domains: list[Domain] = []


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company_id: int


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class DealBase(BaseModel):
    title: str
    amount: int
    open_date: datetime
    close_date: Optional[datetime] = None
    company_id: int
    owner_id: Optional[int]
    stage: StageEnum
    description: Optional[str] = None
    status: StatusEnum


class DealCreate(DealBase):
    pass


class DealUpdate(DealBase):
    pass


class Deal(DealBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    company: str
    email: EmailStr
    phone: str
    details: Optional[str] = None
    status: LeadStatusEnum
    owner_id: Optional[int]
    converted_to_deal_id: Optional[int] = None
    converted_to_contact_id: Optional[int] = None
    converted_to_company_id: Optional[int] = None


class LeadCreate(LeadBase):
    owner_id: int


class LeadUpdate(LeadBase):
    pass


class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class IntegrationResponse(BaseModel):
    integration_id: str


class MessageResponse(BaseModel):
    message: str
