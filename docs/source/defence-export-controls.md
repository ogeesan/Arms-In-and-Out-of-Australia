# Defence Export Controls (DEC)
Defence Export Controls (DEC) is the government body responsible for ensuring Australian arms (goods, technologies, and services) meet Australian export laws both within and outside of Australia.

Between 2015 and 2023, DEC released yearly reports.
From the 2024/2025 financial year DEC began releasing their data quarterly, and added to their report the list of countries that receive these exports.

The most important consideration when examining the DEC data is that this reflects export applications *that were applied and not necessarily fulfilled*.
If KillKorp wants to export hydraulic systems for armoured vehicles to one country, then they may as well submit an export request to DEC for a neighbouring country that might be interested in case their original plans fall through.
Due to this, the total value of permits issued is much larger than the true value of goods exported --- whatever that is.

This is a massive lack of transparency, as we cannot determine how much Australia actually exported, or to where.


## Data extraction process
The DEC publishes PDF files for financial quarters (or financial year, prior to FY2024/2025).
Most of the values have been copy/pasted into `data/defence-export-controls/transcribed/defence-export-controls.yml`.
For the country tables used from FY2024/2025 a Python script has been used to extract those values into a format suitable for copy/paste into the transcribed data.

Pydantic models are used to validate the YAML file.