from datetime import time
from enum import Enum

from pydantic import BaseModel


class Weekdays(str, Enum):
    ALL_WEEK_DAYS = 'ALL WEEK DAYS'.lower()
    MONDAY = 'MONDAY'.lower()
    TUESDAY = 'TUESDAY'.lower()
    WEDNESDAY = 'WEDNESDAY'.lower()
    THURSDAY = 'THURSDAY'.lower()
    FRIDAY = 'FRIDAY'.lower()
    SATURDAY = 'SATURDAY'.lower()
    SUNDAY = 'SUNDAY'.lower()


class CompanyBase(BaseModel):
    name: str | None
    description: str | None
    schedule_start: time | None
    schedule_end: time | None
    schedule_weekdays: Weekdays | None
    phone_number: str | None
    email: str | None
    map_link: str | None
    social_media1: str | None
    social_media2: str | None
    social_media3: str | None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: str | None = None
    description: str | None = None
    schedule_start: time | None = None
    schedule_end: time | None = None
    schedule_weekdays: Weekdays | None = None
    phone_number: str | None = None
    email: str | None = None
    map_link: str | None = None
    social_media1: str | None = None
    social_media2: str | None = None
    social_media3: str | None = None


class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True
