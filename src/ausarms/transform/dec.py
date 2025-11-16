"""Transform the Defence Export Controls data from YAML (Pydantic) into SQL (SQLAlchemy)"""

from pathlib import Path

from sqlalchemy.orm.session import Session

from ausarms import datasource, mappings
from ausarms.models import dec as models
from ausarms.schemas import dec as schemas


class DECTransformer:
    data: list[schemas.FinancialYear]
    filepath = Path("data/transcribed/defence-exports-controls.yml")

    def __init__(self, session):
        self.session = session

    def build_data(self):
        rawdata = datasource.load_multipage_yaml(self.filepath, with_line_numbers=False)
        # mappings.print_unique_names(self.data)
        mappings.remap_dec_data_names(rawdata)
        self.data = [schemas.FinancialYear(**page) for page in rawdata]

    def prepare_database(self) -> None:
        """Populate database"""
        # Populate financial years
        for year in self.data:
            fy = models.FinancialYear(year=year.FinancialYear)
            self.session.add(fy)
        self.session.commit()

        # Populate categories
        category_list = list(schemas.FinancialYear.model_fields)
        for category_name in category_list:
            category = models.Category(name=category_name)
            self.session.add(category)
        self.session.commit()

    def insert_year(self, year: schemas.FinancialYear):
        year_record = (
            self.session.query(models.FinancialYear)
            .filter_by(year=year.FinancialYear)
            .first()
        )
        year_id = year_record.id
        # Export Applications
        # id = Column(Integer, primary_key=True, autoincrement=True)
        # financial_year_id = Column(Integer, ForeignKey("dec_financial_year.id"))
        # category_id = Column(Integer, ForeignKey("dec_category.id"))
        # quarter = Column(Integer, nullable=False)
        # metric = Column(String, nullable=False)
        # value = Column(Numeric)
        export_applications = year.ExportApplications
        export_apps_category = (
            self.session.query(models.Category)
            .filter_by(name="ExportApplications")
            .first()
        )
        add_field(self.session, export_applications, year_id, export_apps_category.id)
        self.session.commit()


def add_field(
    session: Session, category_object: schemas.CoreModel, year_id: int, category_id: int
) -> None:
    """Add the category data into the session.

    Assuming only a single level of nesting within each "category" (a table of values from the dataset)
    this function adds all values to the database.

    Parameters
    ----------
    session : Session
        Current SQL session manager
    category_object : schemas.CoreModel
        An attribute of `FinancialYear`
    year_id : int
        The foreign key id for the financial year
    category_id : int
        The foreign key id for the overarching category
    """
    for quarter in range(1, 5):
        for field in category_object.model_fields_set:
            value = getattr(category_object, field)[quarter - 1]
            if value is None:
                continue
            # print(year.FinancialYear, "Export Applications", quarter, field, value)
            stats = models.QuarterlyStatistics(
                financial_year_id=year_id,
                category_id=category_id,
                quarter=quarter,
                metric=field,
                value=value,
            )
            session.add(stats)
