from sqlalchemy.orm import Session

from ausarms.models.sipri import Country, Expenditure


def get_country(session: Session, name: str) -> Country:
    return session.query(Country).filter_by(name=name).first()


def country_id(session: Session, name: str) -> int:
    return get_country(session, name).id  # type: ignore


def get_military_expenditure(
    session: Session, country_name: str, year: int, measure_type: str
):
    country = get_country(session, country_name)
    if not country:
        return None
    return (
        session.query(Expenditure)
        .filter_by(country=country.id, year=year, measure_type=measure_type)
        .first()
    )
