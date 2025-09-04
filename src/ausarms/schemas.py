"""Pydantic models for Defence Export Control dataset
data/transcribed/defence-exports-controls.yml
"""

# %% Defence Export Controls data
from typing import NamedTuple, Annotated

from pydantic import Field, ConfigDict, BaseModel


ValueType = int | None
QuarterValues = NamedTuple(
    "EntryType",
    [
        ("quarter1", ValueType),
        ("quarter2", ValueType),
        ("quarter3", ValueType),
        ("quarter4", ValueType),
    ],
)


class CoreModel(BaseModel):
    model_config = ConfigDict(
        # validate using alias
        populate_by_name=True,
    )

class ExportApplications(CoreModel):
    """Statistics on export applications received and finalised."""
    ApplicationsReceived: Annotated[
        QuarterValues, Field(..., alias="Applications Received")
    ]
    ApplicationsFinalised: Annotated[
        QuarterValues, Field(..., alias="Applications Finalised")
    ]


class ExportApplicationProcessing(CoreModel):
    percent_non_sensitive: Annotated[
        QuarterValues,
        Field(
            ...,
            alias="percent of export applications that were Non-Sensitive",
        ),
    ]
    percent_sensitive: Annotated[
        QuarterValues,
        Field(..., alias="percent of export applications that were Sensitive/Complex"),
    ]
    percent_non_sensitive_within_15_days: Annotated[
        QuarterValues,
        Field(
            ..., alias="percent of Non-Sensitive applications assessed within 15 days"
        ),
    ]
    percent_sensitive_within_35_days: Annotated[
        QuarterValues,
        Field(..., alias="percent of Sensitive/Complex applications assessed within 35 days"),
    ]


class ExportApplicationApprovals(CoreModel):
    permits_issued_customs: Annotated[
        QuarterValues, Field(..., alias="Permits (Customs Act) Issued")
    ]
    permits_issued_dtc: Annotated[
        QuarterValues, Field(..., alias="Permits (Defence Trade Controls Act) Issued")
    ]
    inprinciple_applications_approved: Annotated[
        QuarterValues, Field(..., alias="In-Principle Applications Approved")
    ]
    export_control_assessments_issued: Annotated[
        QuarterValues, Field(..., alias="Export Control Assessments Issued")
    ]
    advice_government_agencies_issued: Annotated[
        QuarterValues, Field(..., alias="Advice to Government Agencies Issued")
    ]


class ExportApplicationsDenials(CoreModel):
    denials_customs_act: Annotated[QuarterValues, Field(..., alias="Denials (Customs Act)")]
    inprinciple_not_supported: Annotated[
        QuarterValues, Field(..., alias="In-Principle Applications Not Supported")
    ]
    prohibition_dtc: Annotated[
        QuarterValues, Field(..., alias="Prohibition Notices (Defence Trade Controls Act)")
    ]
    prohibition_wmd: Annotated[
        QuarterValues, Field(..., alias="Prohibition Notices (Weapons of Mass Destruction Act)")
    ]
    prohibition_military_end_use: Annotated[
        QuarterValues, Field(alias="Prohibition Notices (Military End Use)")
    ]
    prohibition_publications: Annotated[
        QuarterValues, Field(None, alias="Prohibition Notices (Publications)")
    ]


class ExportsApplicationsUnused(CoreModel):
    withdrawn_inactive_lapsed: Annotated[
        QuarterValues, Field(..., alias="Withdrawn, Made Inactive, or Lapsed")
    ]
    no_further_action: Annotated[
        QuarterValues, Field(alias="No Further Action Required") # not every year has this
    ]


class CertificateStatistics(CoreModel):
    international_import: Annotated[
        QuarterValues, Field(..., alias="International Import Certificates issued")
    ]
    delivery_verification: Annotated[
        QuarterValues, Field(..., alias="Delivery Verification Certificates issued")
    ]
    non_transfer_end_use: Annotated[
        QuarterValues, Field(..., alias="Non-Transfer and End-Use Certificates issued")
    ]
    foreign_end_use: Annotated[
        QuarterValues, Field(..., alias="Foreign End Use Certificates signed")
    ]


class AUSGELStatistics(CoreModel):
    approved: Annotated[QuarterValues, Field(..., alias="AUSGEL - Approved")]
    withdrawn: Annotated[QuarterValues, Field(..., alias="AUSGEL - Withdrawn")]


class AUSGELProcessing(CoreModel):
    certificates: Annotated[QuarterValues, Field(..., alias="Certificates")]
    ausgel: Annotated[
        QuarterValues, Field(..., alias="Australian General Export Licences (AUSGEL)")
    ]


class BrokerRegistration(CoreModel):
    completed: Annotated[QuarterValues, Field(..., alias="Completed")]
    withdrawn: Annotated[QuarterValues, Field(..., alias="Withdrawn")]


class EstimatedValueApproved(CoreModel):
    """Statistics on the estimated value of approved defence permits.
    
    From 2018 applications were required to estimate value across their lifetime, and so a stated caveat of this data is that it's difficult to compare year to year values.

    """
    # these two aren't present in all data
    total: Annotated[QuarterValues, Field(None, alias="Total number permits")]
    number_with_value: Annotated[
        QuarterValues, Field(None, alias="number Permits with Values")
    ]

    percent_with_value: Annotated[
        QuarterValues, Field(..., alias="percent of Defence Permits with a Declared Value")
    ]
    value: Annotated[
        QuarterValues, Field(..., alias="Estimated Value on Approved Defence Permits")
    ]


class Region(CoreModel):
    Asia: Annotated[QuarterValues, Field(None, alias="Asia")]
    Antarctica: Annotated[QuarterValues, Field(None, alias="Antarctica")]
    Australia: Annotated[QuarterValues, Field(None, alias="Australia")]
    Europe: Annotated[QuarterValues, Field(None, alias="Europe")]
    North_America: Annotated[QuarterValues, Field(None, alias="North America")]
    South_America: Annotated[QuarterValues, Field(None, alias="South America")]
    Africa: Annotated[QuarterValues, Field(None, alias="Africa")]
    Oceania: Annotated[QuarterValues, Field(None, alias="Oceania")]


class FinancialYear(CoreModel):
    FinancialYear: str = Field(..., alias="Financial Year")
    ExportApplications: Annotated[ExportApplications, Field(..., alias="Export Applications")]
    ExportApplicationProcessing: Annotated[ExportApplicationProcessing, Field(..., alias="Export Application Processing")]
    ExportApplicationOutcomes: Annotated[ExportApplicationApprovals, Field(..., alias="Export Application Approvals and Assessments")]
    ExportApplicationsDenials: Annotated[ExportApplicationsDenials, Field(..., alias="Export Application Prohibitions and Denials")]
    ExportsApplicationsUnused: Annotated[ExportsApplicationsUnused, Field(..., alias="Export Applications Withdrawn, Made Inactive, Lapsed and No Further Action Required")]
    CertificateStatistics: Annotated[CertificateStatistics, Field(..., alias="Certificate Statistics")]
    AUSGELStatistics: Annotated[AUSGELStatistics, Field(..., alias="Australian General Export Licences (AUSGEL) Statistics")]
    AUSGELProcessing: Annotated[AUSGELProcessing, Field(..., alias="Certificates and Australian General Export Licences (AUSGEL) Processing")]
    BrokerRegistration: Annotated[BrokerRegistration, Field(..., alias="Broker Registration")]
    EstimatedValueApproved: Annotated[EstimatedValueApproved, Field(..., alias="Estimated Value of Approved Defence Permits")]
    Region: Annotated[Region, Field(..., alias="Export Permits Issued to End Users by Region")]
