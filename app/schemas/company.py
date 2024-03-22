from datetime import time
from enum import Enum

from pydantic import BaseModel


class Weekdays(str, Enum):
    ALL_WEEK_DAYS = 'all_week_days',
    MONDAY = 'monday',
    TUESDAY = 'tuesday',
    WEDNESDAY = 'wednesday',
    THURSDAY = 'thursday',
    FRIDAY = 'friday',
    SATURDAY = 'saturday',
    SUNDAY = 'sunday'


class CompanyBase(BaseModel):
    name: str | None
    description: str | None
    schedule_start: time | None
    schedule_end: time | None
    schedule_weekdays: Weekdays | None = Weekdays.ALL_WEEK_DAYS
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


class CompanyPaginated(BaseModel):
    count: int
    results: list[Company]
    next_page: str | None = None
    prev_page: str | None = None
