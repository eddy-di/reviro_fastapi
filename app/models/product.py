from sqlalchemy import (
    DECIMAL,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    price = Column(DECIMAL(precision=10, scale=2))
    discount = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'))

    company = relationship('Company', back_populates='products')
