from sqlalchemy import Column, Integer, String, ForeignKey, Numeric

from .base import Base


class FinancialYear(Base):
    __tablename__ = "dec_financial_year"
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String, nullable=False, unique=True)


class Category(Base):
    __tablename__ = "dec_category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)


class QuarterlyStatistics(Base):
    """Table of all of the quarterly statistics"""

    __tablename__ = "dec_statistics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    financial_year_id = Column(Integer, ForeignKey("dec_financial_year.id"))
    category_id = Column(Integer, ForeignKey("dec_category.id"))
    quarter = Column(Integer, nullable=False)
    metric = Column(String, nullable=False)
    value = Column(Numeric)
