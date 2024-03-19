from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from app.config.database import Base


class Weekdays(PyEnum):
    ALL_WEEK_DAYS = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True)
    description = Column(Text)
    schedule_start = Column(Time)
    schedule_end = Column(Time)
    schedule_weekdays = Column(Enum(Weekdays))
    phone_number = Column(String)
    email = Column(String)
    map_link = Column(String)
    social_media1 = Column(String)
    social_media2 = Column(String)
    social_media3 = Column(String)

    products = relationship('Product', back_populates='company', cascade='all, delete')
