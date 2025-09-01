# Arms in and out of Australia - a data project

- Python: `pandas`, `numpy`, `sqlalchemy`, `matplotlib`
- SQL: SQLite (and eventually Postgres) with Python's `sqlalchemy`
- Typst: Generating .pdf

To grow my professional capabilities I'm using SQL

To grow my sense of humanity, I'm looking at the military industrial complex in Australia.

This project has made minimal use of AI tools in writing the code, and no AI in the writing of the report.

Typst is like LaTeX but fun to use.
My project `scilayout` is used to build the figures that are then used by report.typ to compile report.pdf.


https://github.com/thedatafae/military-spending-sql-osint/blob/main/analysis_report.pdf

> [!NOTE]
> The military expenditure dataset from SIPRI cannot be included within the repository because SIPRI limits reproduction to a maximum of 10%. The dataset can be obtained [here](https://www.sipri.org/databases/milex) and should be placed in `data/raw/`.
## Report
[Typst](typst.app) was used to generate the `ausarms-report.pdf`. `assets/references.bib` was manually curated.

## Data cleaning
SIPRI data was used to generate the `countries` table. 

While building the database it became apparent that the Solomon Islands, Tonga, and Vanuatu are not present in the military expenditure dataset while they are present in the transfers.

Vanuatu, Tonga, and the Solomon Islands are added to the countries table as they do not appear in SIPRI's military expenditure dataset.

## Future Improvements

- The Department of Defence's Defence Export Controls (DEC) [publishes yearly statistics](https://www.defence.gov.au/about/accessing-information/export-permit-statistics) on permits for arms exports.
- The Arms Trade Treaty Annual Reports have yearly data https://thearmstradetreaty.org/annual-reports.html?templateId=209826 for reporting.
- The Australian Bureau of Statistics publishes [Defence Industry Account](https://www.abs.gov.au/statistics/economy/national-accounts/australian-defence-industry-account-experimental-estimates/2023-24)
- AusTenders has [an API](https://github.com/austender/austender-ocds-api) that could be used to generate better company specific data.
