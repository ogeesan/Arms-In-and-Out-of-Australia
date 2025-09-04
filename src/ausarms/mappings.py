"""Remap headings and categories in the Defence Exports Controls data to normalised names."""

headings_mappings = {
    "Value of Approved Defence Permits": "Estimated Value of Approved Defence Permits",
    "Value of Approved Defence Permits by Year": "Estimated Value of Approved Defence Permits",
    "Export Permits Issued to End Users by Continent": "Export Permits Issued to End Users by Region",
    "Export Application Outcomes": "Export Application Approvals and Assessments",
    "Certificates Issued": "Certificate Statistics",
}

category_mappings = {
    "AUSGEL - Application withdrawn by applicant": "AUSGEL - Withdrawn",
    "Applications finalised": "Applications Finalised",
    "Applications received": "Applications Received",
    "no further action required": "No Further Action Required",
    "Australian General Export Licenses (AUSGEL)": "Australian General Export Licences (AUSGEL)",
    "Foreign End User Certificates Signed": "Foreign End Use Certificates signed",
    "Foreign End User Certificates signed": "Foreign End Use Certificates signed",
    "In-Principle Applications not supported": "In-Principle Applications Not Supported",
    "Permits refused (Defence Trade Controls Act)": "Prohibition Notices (Defence Trade Controls Act)",
    "Permits refused (Customs Act)": "Denials (Customs Act)",
    "Prohibitions Notices (Military End-Use)": "Prohibition Notices (Military End Use)",
    "Withdrawn, made inactive, lapsed": "Withdrawn, Made Inactive, or Lapsed",
    "Withdrawn, Made Inactive or Lapsed": "Withdrawn, Made Inactive, or Lapsed",
    "percent of export applications that were Non-Sensitive/Non-Complex": "percent of export applications that were Non-Sensitive",
    "percent of export applications that were Non-sensitive": "percent of export applications that were Non-Sensitive",
    "percent of export applications that were Sensitive/complex": "percent of export applications that were Sensitive/Complex",
    "Value of Approved Defence Permits": "Estimated Value on Approved Defence Permits",
    "Broker Registration - Withdrawn": "Withdrawn",
    "Broker Registrations - Withdrawn": "Withdrawn",
    "Broker Registration - Received": "Received",
    "Broker Registration - Completed": "Completed",
}


def remap_dec_data_names(data: list[dict]) -> None:
    """Remap the headings and categories in the Defence Exports Controls data to normalised names."""
    for page in data:
        # remap headings
        for old_heading, new_heading in headings_mappings.items():
            if old_heading in page:
                page[new_heading] = page.pop(old_heading)

        # remap categories
        for heading in page:
            if heading == "Financial Year":
                continue
            for old_category, new_category in category_mappings.items():
                if old_category in page[heading]:
                    page[heading][new_category] = page[heading].pop(old_category)


def print_unique_names(data: list[dict]) -> None:
    """Print all unique headings and categories in the Defence Exports Controls data."""
    # Build dict of all names
    data_org = {}
    for page in data:
        financial_year = page["Financial Year"]
        headings = list(page.keys())
        categories = []
        for heading in headings:
            if heading == "Financial Year":
                continue
            categories.append(page[heading].keys())
        data_org[financial_year] = {"headings": headings, "categories": categories}

    # find all unique categories
    unique_categories = set()
    for financial_year, names in data_org.items():
        for category in names["categories"]:
            unique_categories.update(category)
    unique_categories = list(unique_categories)
    unique_categories.sort()

    # find unique headings
    unique_headings = set()
    for financial_year, names in data_org.items():
        unique_headings.update(names["headings"])
    unique_headings = list(unique_headings)
    unique_headings.sort()

    print(f"Unique categories ({len(unique_categories)}):")
    for category in unique_categories:
        print(f" - {category}")
    print(f"\nUnique headings ({len(unique_headings)}):")
    for heading in unique_headings:
        print(f" - {heading}")
