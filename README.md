# Arms in and out of Australia - a data project
Australia's arms industry is less transparent than other countries, even the United States and the United Kingdom.
This project aims to aggregate all of the data on Australian arms that does exist into something usable by anyone.

To grow my professional capabilities I'm building a project that makes use of SQL to manage data.
To focus my energies onto something I think is important and to also share that thing, I'm looking at the data of the Australian arms industry.

<h1 align="center">
  <a href="Arms%20In%20and%20Out%20of%20Australia.pdf">Read the Report here</a>
</h1>

This project primarily makes use of:
- Python: `pandas`, `numpy`, `sqlalchemy`, `matplotlib`
- SQL: SQLite (and eventually Postgres) with Python's `sqlalchemy`
- Typst: Generating .pdf

This project has made minimal use of AI tools in writing the code, and no AI in the writing of the report.

Included usage in my project is [`scilayout`](https://github.com/ogeesan/scilayout), my package for building figures/visualisations in real size (is a part of project requirements).

> [!NOTE]
> The military expenditure dataset from SIPRI cannot be included within the repository because SIPRI limits reproduction to a maximum of 10%. The dataset can be obtained [here](https://www.sipri.org/databases/milex) and should be placed in `data/raw/`.

## Pre-requisites
- Typst: [Install](https://github.com/typst/typst?tab=readme-ov-file#installation)
- uv: [Install](https://docs.astral.sh/uv/)

1. `uv sync` to prepare the environment 
2. Run `main.py` to build the database, generate the figures, and generate the report
3. Open `Arms In and Out of Australia.pdf` to read the report

## Future Improvements
- The Department of Defence's Defence Export Controls (DEC) [publishes yearly statistics](https://www.defence.gov.au/about/accessing-information/export-permit-statistics) on permits for arms exports.
- The Arms Trade Treaty Annual Reports have yearly data https://thearmstradetreaty.org/annual-reports.html?templateId=209826.
- The Australian Bureau of Statistics publishes [Defence Industry Account](https://www.abs.gov.au/statistics/economy/national-accounts/australian-defence-industry-account-experimental-estimates/2023-24).
- AusTenders has [an API](https://github.com/austender/austender-ocds-api) that could be used to generate better company specific data.


```
data/
  source/     # the data extracted itself
    defence-export-controls/
    australian-bureau-statistics/
    arms-trade-treaty/
    strategic-policy-research-institute/
  extracted/  # csv/json extracted
```

## Data organisation
- data/
  - `defence-export-controls/`
    - `source/` : raw files downloaded from the source
    - `extracted/` : extracted using a script
    - `transcribed/` : manually copy/pasted or written down
    - `exported/` : data cleaned and ready for usage