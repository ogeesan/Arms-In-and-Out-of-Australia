# %%
"""Build SQLdatabase using data acquired from SIPRI and ASPI."""

from pathlib import Path

from ausarms import datasource, models, database


# noinspection D
def build_database(db_type):

    datasource.download_sipri_milex_data()
    # For SQLite, remove the old database file to start fresh
    filename = "ausarms.db"
    if db_type == "sqlite":
        if Path(filename).exists():
            Path(filename).unlink()
            print("Removed existing database file.")

    engine = database.create_engine(db_type)
    SessionFactory = database.create_session(engine)

    countries = datasource.build_country_table()
    countries["Country"] = countries["Country"].apply(datasource.normalise_country_name)
    print("Populating database...")
    models.Base.metadata.create_all(engine)

    with SessionFactory.begin() as session:
        # Build countries
        country_id_mapping = {}
        for index, countryrow in countries.iterrows():
            country_name = countryrow["Country"]
            country = models.Country(
                name=countryrow["Country"],
                continent=countryrow["Continent"],
                region=countryrow["Region"],
            )
            session.add(country)
            session.flush()  # to get the id
            country_id_mapping[country_name] = country.id

        # Build military expenditure
        for measure in datasource.measure_types:
            data = datasource.load_military_expenditure_data(measure)
            data["Country"] = data["Country"].apply(datasource.normalise_country_name)
            for country_name in countries["Country"]:
                if country_name in ["Solomon Islands", "Tonga", "Vanuatu"]:
                    continue
                country_id = country_id_mapping[country_name]
                index = data.index[data["Country"] == country_name][0]
                if measure in ["share_of_gov_spending", "per_capita"]:
                    start_year = 1988
                else:
                    start_year = 1949
                for year in range(start_year, 2024 + 1):
                    year_data = data.at[index, year]
                    if isinstance(year_data, str):
                        continue
                    expense = models.Expenditure(
                        country=country_id,
                        year=year,
                        expenditure=year_data,
                        measure_type=measure,
                    )
                    session.add(expense)

        # Build transfers
        for direction in ["incoming", "outgoing"]:
            data = datasource.load_sipri_traderegister(direction)
            data["Recipient"] = data["Recipient"].apply(datasource.normalise_country_name)
            data["Supplier"] = data["Supplier"].apply(datasource.normalise_country_name)
            for index, row in data.iterrows():
                transfer = models.Transfer(
                    recipient=country_id_mapping[row["Recipient"]],
                    supplier=country_id_mapping[row["Supplier"]],
                    year_ordered=row["Year of order"],
                    weapon_description=row["Weapon description"],
                    number_ordered=row["Number ordered"],
                    number_delivered=row["Number delivered"],
                    status=row["status"],
                    tiv_total_order=row["SIPRI TIV for total order"],
                    tiv_delivered=row["SIPRI TIV of delivered weapons"],
                )
                session.add(transfer)

        # Build exports
        data = datasource.load_aspi_cod_table()

        for index, row in data.iterrows():
            export = models.Export(
                company=row["Company"],
                recipient=row["Recipient"],
                description=row["Export Description"],
                year_ordered=row["Year Ordered"],
                year_delivered=row["Year Delievered"],  # sic
                value=row["Value (AUDm)"],
                category=row["Category"],
                adf_used=row["Current or prior ADF-use"],
                donation=row["Donation"],
            )
            session.add(export)

    print("Data population complete.")

def main():
    db_type = "sqlite"  # "sqlite" or "postgresql"
    build_database(db_type)

if __name__ == '__main__':
    main()