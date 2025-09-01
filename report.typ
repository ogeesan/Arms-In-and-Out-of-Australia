// #set text(font: "Atkinson Hyperlegible", size: 10pt)
// #set text(font: "Readex Pro", weight: "light", size: 11pt)
#set text(font: "IBM Plex Sans")
#import "@preview/gentle-clues:1.2.0": code
#align(center, text(18pt, weight: "bold")[Arms in and out of Australia])
#align(center)[George Stuyt]
#align(right)[
  #text(8pt, font: "Lucida Console", fill: luma(70%))[
    Generated #datetime.today().display()
  ]
]


// #set page(margin: (right: 9cm))
#set par(justify: true)

// Create codebox function to show data approach
#let codebox(title: [], body) = {
  figure(
    code(title: [Codebox #context counter(figure.where(kind: "codebox")).get().first(): ] + title, body),
    kind: "codebox",
    supplement: [Codebox]
  )
}
#show figure.caption.where(kind: image): set align(left)
#show figure.caption.where(kind: image): set par(justify: false)

#let figsource(body) = {
  set text(style: "italic")
  [Source: ] + body
}
#let pl(body) = {
  set text(style: "italic")
  body + [.]
}
// #show "The Strategist": text(style: "italic")[The Strategist]


= Introduction
In 2018 the Australian Government announced its plan to become one of the top 10 arms exporters in the world @ausgovDefenceExportStrategy2018.
Since then, Australia's share of the global international arms trade has increased by 54%, ranking it 17 in the world @sipriTrendsInternationalArms2024.
Modern warfare's civilian death rate is 25% to 50% @Khorram-ManeshEstimatingCivilianCasualties2021 and its negative impacts are much broader.
For all of the strategic analysis we can do there are factual realities about who is doing the dying.
Australia is a growing arms exporter and Australians need to be aware of what this means.

This document is two things.
Firstly, it is an analysis of the data on the Australian arms industry designed to give readers an insight into what Australia is undertaking and the lack of clarity in the data about this.
Secondly, it is a "toy-project" which is a programming project to learn and showcase competency to recruiters.
It is for this second reason this report contains boxes like @cb-techstack, which are code or pseudo-code used to process and generate the data/graphs.
These boxes are irrelevant to readers looking only for information on Australia's arms industry, but are relevant for individuals who are looking to see if I can walk the programming talk.
It is for this reason that the report focuses largely on data, and what might be considered my opinion is relegated to the footnotes.

#codebox(title: "Tech stack")[
  - SQLite for SQL database.
  - Python: including `sqlalchemy`, `matplotlib`, `pandas`, and `scilayout`.
  - Typst to produce this PDF file.
]<cb-techstack>

= The data on Australia's place in the arms trade
The premier location for understanding global arms trade is in the databases maintained by the Stockholm International Peace Research Institute (SIPRI).
They use government reports and media reports to build data on every nation.
In this section, we will examine three datasets on Australia and its arms: government military expenditure, government arms transfers, and industry exports (from a different data source).

== Government military expenditure
One way to examine how Australia's investment in armaments is going is to look at government military expenditure @sipriMilitaryExpenditureDatabase.

#figure(
  image("images/milex_australia.svg"),
  caption: [
    Australia's government defence expenditure versus global trends.
    #pl[a] Expenditure as percentage of government spending. Blue, Australia; Grey, global median.
    #pl[b] Expenditure as per capita. Values are AUD in 2023.
    #figsource[SIPRI]
    ],
)<fig-milex-median>

According to expenditure as a percentage of total government spending, Australia's expenditure levels are right about level with the global median at just below 6% (#ref(<fig-milex-median>)a).
However, if we consider expenditure per capita (#ref(<fig-milex-median>)b) we see that Australia is spending much more.
#footnote[
  The question I ask is this: is increased economic power a good enough reason to keep spending so much on "defence"?
  If Australia has more money to throw around than most, what are we doing still throwing it at military expenditure?
]
Certainly, the United States thinks that Australia needs to spend more on its military.
This data is government expenditure, which is only one measure of Australia's military imports and exports.
However, it is also worthwhile to step aside from trends for a moment and consider the actual amount of money being spent here.
// Thales 5844411504
// Raytheon 21712664629
// Lockheed 2376660647
Since 2020, the Australian Government @ausgovAusTenderThales paid the big three arms mega-corporations Thales, RTX (formerly Raytheon), and Lockheed Martin a combined \$29,933,736,780 (29.9 billion).
Depending on one's perspective this value may be obscene or under-funding.

#codebox(title: [Building data models with `sqlalchemy`'s object-relational mapping])[
  Following initial data wrangling in `ausarms/datasource.py`, `scripts/build_database.py` was used to build the SQL database using models defined in `ausarms/models.py`.
  ```python
  # ausarms/models.py
  from sqlalchemy.orm import declarative_base
  Base = declarative_base()
  class Country(Base):
    """All countries, populated from SIPRI's global military expenditure data."""
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
  ```
]<cb-orm>


== Major weapons transfer
The exchange of weapons themselves can be examined using SIPRI's arms transfer database @sipriArmsTransferDatabase.
This database records "major conventional weapons" transfers between nations.
Along with each transfer, SIPRI defines a value they call the trend-indicator value (TIV), which is designed to be a measure of military capability rather than financial exchange @sipriMeasuringArmsTransfers2012.

#figure(
  image("images/transfer_australia.svg"),
  caption: [
    SIPRI's arms transfer data for Australia.
    #pl[a] Australian arms export volume. Trend Indicator Value (TIV) measures military resources as calculated by SIPRI. Bars show quantity ordered (by other nation) in the given year, red line shows average for the decade.
    #pl[b] Weapons category contribution across all records of Australia outgoing transfers.
    #figsource[SIPRI]
    ]
)<fig-transfer>

This is problematic for our questions given that Australia does not have an arms industry that produces tanks.
Although there seems to be a slight upwards trend in the decade-average (#ref(<fig-transfer>)a), this is not large enough to be particularly insightful.
However, it is apparent in the types of arms being recorded (#ref(<fig-transfer>)b) that, as described by SIPRI, this data covers only "major conventional weapons".

One difficulty in describing arms trade in terms of yearly transfer is that orders are placed for fulfilment well in advance.
Orders can take years to fulfil.


But an arms industry is much larger than that.
Arms transfer, in which individual items.
For example, SIPRI data does not include arms components, such as items in the F-35 Joint Strike Fighter jet.
Participation in the arms industry is not simply a matter of buying guns or even just selling them.

#codebox(title: [Retrieving data from SQL database using object-relational mapping])[
  SQL queries using orm 
  ```python
  from sqlalchemy.orm import sessionmaker
  from ausarms import crud
  session = sessionmaker()  # pseudo-code
  df_aus = pandas.read_sql(
        session.query(crud.Expenditure)
        .join(crud.Country)
        .filter(crud.Country.name == 'Australia',
                crud.Expenditure.measure_type == 'per_capita')
        .statement,
        session.bind
  )
  ```
]<cb-query>


== The Australian arms industry
It is well recognised that the Australian Government lacks transparency when it comes to Australian arms exports @conversationWhatWeKnow2023 @hellyerDemystifyingAustraliasDefence.
For this reason, an important source in this project is a dataset from the Australian Strategic Policy Institute (ASPI) which aimed to catalogue Australian arms exports across a broad range @aspiCostOfDefence2022, from major exports like Bushmaster troop carriers to services like the testing of combat helmets.

This is particularly important when we consider a system like the F-35 jet.
It is Australia's (and much of NATO's) latest attack jet, boasting advanced stealth capabilities and over eight tonnes of explosive carrying capacity.
Australia is one of eight nations that build parts for the F-35, which is ultimately constructed by Lockheed Martin.
The F-35 is constructed with a complex global supply chain where Lockheed Martin contracts the construction of components out to different companies in different countries.
Since 2006, more than 75 companies in Australia have participated as part of this, yielding more than AUD\$5,000,000,000 (five billion) in revenue @ausgovF35BillionMilestone2025.
For example, Rosebank (located in Bayswater, Victoria) constructs the actuators for the bomb-bay doors, and Ferra (located in Brisbane, Queensland) builds weapons adaptors for carrying missiles inside the bomb-bay.
The nature of the supply chain means that every single F-35 in operation has parts made in Australia.
The arms trade is not simply a matter of building a gun and selling it: the globalisation of trade and industry has spread the manufacturing responsibility for complex arms across multiple nations.
#footnote[
  Therefore, when the Prime Minister and others have stated that the parts Australia supplies into the global F-35 program are "non-lethal", they are correct.
  //https://www.abc.net.au/news/2025-08-14/australia-defence-export-permits-to-israel-gaza-war/105628320
  We merely build the actuators for the doors that open to kill civilians, not the bombs themselves.
]
Importantly, SIPRI's data does not collect this broader industry information, and so ASPI's dataset may give a more accurate picture of the state of the arms industry in Australia.

#figure(
  image("images/cod_data.svg"),
  caption: [
    Australian arms industry exports.
    #pl[a] Number of exports ordered per year.
    #pl[b] Distribution of categories of exports.
    #figsource[ASPI]
  ]
)<fig-cod>

It would appear that this dataset shows a major increase in volume of export orders being made rising rapidly from 2000 (#ref(<fig-cod>)a).
However, it is worth noting that this database is not exhaustive and is entirely reliant on media reports.
#footnote[
  The ASPI compiled this database and stated "it will show that Australia has a robust, internationally competitive defence industry that has won export success far beyond the headline stories" @hellyerDemystifyingAustraliasDefence.
  I am sure that they want this data to show that Australia's arms industry is growing nicely and ready for more.
]
The F-35 program is an important component of the Australian arms industry, with 55 of the 141 exports recorded related to the F-35 program.
The data also highlights how important it is to examine the arms industry more broadly than government expenditure or SIPRI's TIV measures, as most of Australia's arm trade activity happens in terms of subcomponents (parts of weapon systems) rather than platforms (complete weapons).

#codebox(title: [Making graphics with `pandas` and `matplotlib`])[
  ```python
  def plot_category_data(ax: matplotlib.axes.Axes, df: pandas.DataFrame) -> None:
      data = df.groupby('category').id.count()
      data.sort_values(ascending=False, inplace=True)
      ax.barh(data.index, data.values / data.values.sum() * 100,
              color=ausarms.vis.palette.rgb('Australia'))
      ax.set_ylim(-.5, len(data))
      ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter(100, decimals=0))
      seaborn.despine(ax=ax, left=True, offset=5)
  
  fig = scilayout.figure()
  ax_categories = fig.add_panel((10, 1.5, 5, 5), method='size')  # in centimetres
  plot_category_data(ax_categories, df_aspi)

  ```
]<cb-plot-function>

= Conclusion
The Australian Government states that it is proceeding with what it calls "one of the most complex and consequential industrial transformations in Australian history" to build our submarine capabilities and ensure we are "integrating Australian industry into US and UK supply chains" @ausgovIndustrialSubmarines2025.
And industrial transformations are only one component of our national goals surrounding the arms industry.
Consider, for example, education.
Programs like Nuclear-Powered Submarine Propulsion Challenge and SUBS In Schools @ausgovNuclearSubmarineChallenge2023 @reaSubsInSchools2015 are designed to get bright young Aussie kids involved with Australia's future in submarine warfare early on.
#footnote[
  Getting submarines into schools is an important part of normalising submarines, which the more you think about the crazier it gets.
]
Similarly, universities are receiving increasing amount of financial interest from the arms industry and Department of Defence @troathPoliticalEconomyAustralian2023.
It is now well known that there is a "revolving door" enabling people to move between powerful positions in the military,  Government, and arms industry @abcRevolvingDoor2023.
There is a lot of money to be made.
When arms manufacturing has growing power in an economy and is entrenched in the political establishment, we call that a military-industrial complex.
// #footnote[The minister responsible for the 2018, Christopher Pyne, went on to make headlines for their involvement in the arms industry following his departure from politics @abcRevolvingDoor2023.]
Australia's rank of 17 in the global arms trade constitutes 0.5% of the global total according SIPRI @sipriTrendsInternationalArms2024.#footnote[
  It may be tempting to say that since Australia's overall contribution is so small it does not matter.
  In my view, the ethics of trading arms has little to do with the volume of the arms being traded.
]
However, regardless of Australia's size, this growth is happening @troathPoliticalEconomyAustralian2023.
Tying together strategic interests and economic interests is a dangerous joyride flush with cash and ethical problems.
Once they become deeply entangled it sets the stage for dangerous and destructive politics driven by vested interests @hartungArmsDreamRepresentative2022.

The slaughter of Gaza is a prime example of where the industrial considerations contaminate.
It has been embarrassing to see government ministers stumble over attempted reasoning about how "we do not sell weapons to Israel".
What they really mean is that we build essential #emph[parts] for weapons systems, which according to these ministers are not #emph[weapons], and that we do not #emph[sell] to Israel but instead selling to Lockheed Martin or the United States (who go on to sell them to Israel).

#quote(attribution: [Defence Minister Richard Marles @abcMurkyDebateExport2024], block: true)[
  // We're an F-35 country and we have been for decades.
  // That's a multilateral arrangement, organised by Lockheed Martin.
  We need to be really clear about how complex this becomes very quickly ...
  I mean the reality is that in the world today we live in a very complex global supply chain, that is actually very much the case in relation to the F-35s.
]
And Minister Marles is right.
It is complex, complex enough that our hands are now tied.
This is the point, the machine is so big now it cannot be stopped.
Not for anything, not even what the International Court of Justice might rule is a genocide.
This is what tying together weapons building and economic interests gets you.

// In 1961 the President of the United States gave an address that coined the term "military-industrial complex", where he described a need for the development of a "mighty" military establishment.
// In it he stated that:
// #quote(attribution: [
//   President Dwight D. Eisenhower#footnote[Eisenhower oversaw major military growth during his presidency, but was kind enough to leave a warning to others about his own legacy.]
//   ], block: false)[
//   We recognize the imperative need for this development.
//   Yet we must not fail to comprehend its grave implications.
// ]

// The grave implication was massive influence stemming from powerful military and industrial powers.
// The "imperative need" that Eisenhower was referring to was the perceived threat of the Soviet Union, but "imperative" is a fitting word for us today too.
// It is the assumed imperative our nation embraces for #emph[economic growth at all costs], whether by upholding ecologically destructive systems or by growing our capacity to build tools to kill people.

In this small project where I am learning some important programming skills, I have also explored some important data on the trends in Australia's arms industry.
I hope this has been an informative report, regardless of your initial reasons for reading it.

#pagebreak()
#bibliography(
  "references.bib",
  title: [References],
  style:"iso-690-numeric",
  // style: "iso-690-author-date",
  // style: "modern-humanities-research-association",
)

// == Appendix

// === SIPRI database protocol
// The Arms Transfer Database @sipriArmsTransferDatabase data was collected using the web-interface.
// Two datasets were downloaded: one where Australia is the Recipient and another where Australia is the Supplier.
// Note that these datasets do not contain, if there are any, transfers where Australia was a joint supplier together with other nations as these transfers have the Supplier listed as `'multiple'`.

// The military expenditure dataset was used to build @sipriMilitaryExpenditureDatabase the database.
// However, SIPRI limits the reproduction of this dataset to a maximum of 10% and so it cannot be included with this repository.
