"""Models for SQL database of Australian arms trade data."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

Base = declarative_base()

class Country(Base):
    """All countries, populated by SIPRI's global military expenditure database.

    Manual entries for Vanuatu, Solomon Islands, and Tonga are made in datasource.
    """

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    continent = Column(String)
    region = Column(String)


class Expenditure(Base):
    """SIPRI military expenditure data."""

    __tablename__ = "sipri_military_expenditure"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(Integer, ForeignKey("countries.id"))
    year = Column(Integer)
    expenditure = Column(Float)
    measure_type = Column(String)
    """Type of measure: "current_usd", "share_of_gov_spending", "share_of_gdp", "per_capita"""


class Transfer(Base):
    """SIPRI arms transfer database.

    Catalogs the weapon transfer/trade between nations.
    """

    __tablename__ = "sipri_aus_transfers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipient = Column(Integer, ForeignKey("countries.id"))
    supplier = Column(Integer, ForeignKey("countries.id"))
    year_ordered = Column(Integer)
    weapon_description = Column(String)
    number_ordered = Column(Integer)
    number_delivered = Column(Integer)
    status = Column(String)
    tiv_total_order = Column(Float)
    tiv_delivered = Column(Float)


class Export(Base):
    """ASPI's Cost of defence database of Australian arms exports.

    Includes services and other arms-related exports.
    """

    __tablename__ = "aspi_cod_exports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String)
    recipient = Column(String)
    description = Column(String)
    year_ordered = Column(Integer)
    year_delivered = Column(Integer)
    value = Column(Float)
    category = Column(String)
    adf_used = Column(Boolean)
    donation = Column(Boolean)
