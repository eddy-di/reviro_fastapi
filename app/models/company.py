from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Text, Time
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from app.config.database import Base


class Weekdays(PyEnum):
    ALL_WEEK_DAYS = 'ALL WEEK DAYS'.lower()
    MONDAY = 'MONDAY'.lower()
    TUESDAY = 'TUESDAY'.lower()
    WEDNESDAY = 'WEDNESDAY'.lower()
    THURSDAY = 'THURSDAY'.lower()
    FRIDAY = 'FRIDAY'.lower()
    SATURDAY = 'SATURDAY'.lower()
    SUNDAY = 'SUNDAY'.lower()


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True)
    description = Column(Text)
    schedule_start = Column(Time)
    schedule_end = Column(Time)
    schedule_weekdays = Column(
        ENUM(Weekdays),
        default=Weekdays.ALL_WEEK_DAYS,
        nullable=True
    )
    phone_number = Column(String)
    email = Column(String)
    map_link = Column(String)
    social_media1 = Column(String)
    social_media2 = Column(String)
    social_media3 = Column(String)

    products = relationship('Product', back_populates='company', cascade='all, delete')

    def __str__(self):
        result = (
            f'"name": {self.name},\n'
            f'"description": {self.description},\n'
            f'"schedule_start": {self.schedule_start},\n'
            f'"schedule_end": {self.schedule_end},\n'
            f'"schedule_weekdays": {self.schedule_weekdays},\n'
            f'"phone_number": {self.phone_number},\n'
            f'"email": {self.email},\n'
            f'"map_link": {self.map_link},\n'
            f'"social_media1": {self.social_media1},\n'
            f'"social_media2": {self.social_media2},\n'
            f'"social_media3": {self.social_media3}\n'
        )
        return result
