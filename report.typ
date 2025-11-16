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
    supplement: [Codebox],
  )
}
#show figure.caption.where(kind: image): set align(left)
#show figure.caption.where(kind: image): set par(justify: false)

#let figsource(body) = {
  set text(style: "italic")
  [Source: ] + body
}
#let pl(body) = {
  set text(style: "italic", weight: "bold")
  body + [)]
}
// #show "The Strategist": text(style: "italic")[The Strategist]



= Introduction
In 2018 the Australian Government announced its plan to become one of the top 10 arms exporters in the world @ausgovDefenceExportStrategy2018.
Since then Australia's share of the global international arms trade has increased by 54%, ranking it 17 in the world @sipriTrendsInternationalArms2024.
Modern warfare's civilian death rate is 25% to 50% @Khorram-ManeshEstimatingCivilianCasualties2021 and its negative impacts are much broader.
For all of the strategic analysis we can do about Australia's "defence posture" there are factual realities about who is doing the dying.
Australia is a growing arms exporter and Australians need to be aware of what this means.

This report is two things.
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
  ],
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

Additionally, SIPRI's dataset contains various values from historical item transfers, such as donations of vehicles to museums.

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
Between 2006 and 2025, more than 75 companies in Australia have participated as part of this, yielding more than AUD\$5,000,000,000 (five billion) in revenue @ausgovF35BillionMilestone2025.
For example, Rosebank (located in Bayswater, Victoria) constructs the actuators for the bomb-bay doors, and Ferra (located in Brisbane, Queensland) builds weapons adaptors for carrying missiles inside the bomb-bay.
The nature of the supply chain means that every single F-35 in operation around the world has parts made in Australia.
The arms trade is not simply a matter of building a gun and selling it: the globalisation of trade and industry has spread the manufacturing responsibility for complex arms across multiple nations.
#footnote[
  Therefore, when the Prime Minister and others have stated that the parts Australia supplies into the global F-35 program are "non-lethal", he is correct.
  //https://www.abc.net.au/news/2025-08-14/australia-defence-export-permits-to-israel-gaza-war/105628320
  We merely build the actuators for the doors that open to kill civilians, not the bombs themselves.
]
Importantly, SIPRI's data does not collect this broader industry information, and so ASPI's dataset may give a more accurate picture of the state of the arms industry in Australia.

#figure(
  image("images/cod_data.svg"),
  caption: [
    Australian arms industry exports manually curated by ASPI.
    #pl[a] Number of exports ordered per year.
    #pl[b] Distribution of categories of exports.
    #figsource[ASPI]
  ],
)<fig-cod>

It would appear that this dataset shows a major increase in volume of export orders being made rising rapidly from 2000 (#ref(<fig-cod>)a).
However, it is worth noting that this database is not exhaustive and is almost entirely reliant on media reports.
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

The data also cannot capture important legislative changes that are occurring.
//Defence and Strategic Goods List (DSGL)
In April of 2024 Parliament passed the Defence Trade Controls Amendment Bill.
This bill effectively gives a permit exemption to arms industry exports to the United States and United Kingdom.
This means Australia can export arms to the United States freely, and also that whatever it is that the United States does with those is none of our business.
This has already been observed with
and there is a possibility that

The slaughter of Gaza is a prime example of where the industrial considerations contaminate.
It has been embarrassing to see government ministers stumble over attempted reasoning about how "we do not sell weapons to Israel".
What they really mean is that we build essential #emph[parts] for weapons systems, which according to these ministers are not #emph[weapons], and that we do not #emph[sell] to Israel but instead selling to Lockheed Martin or the United States (who go on to sell them to Israel).

Australia is smuggling F-35 parts to Israel in passenger jets @declassifiedSecretCargoInside2025.
I would like to believe that the average Aussie recognises this is insanity.

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

== The Future

It is very reasonable that Australia should at least examine its arms exports in the context of nations undergoing active investigation for crimes against humanity and genocide.

Firstly, transparency.
Information on the arms trade is scarce, and the data that does exist lacks real detail.
In the end, Australians are left guessing as to what is being sold where and for what purpose, which is exactly the problem.
Secondly, governance.
Australia has no systems to monitor or react to the usage of its arms exports.
This is effectively an excuse to sell arms to the United States and simply say "be chill, it's to our allies".
Thirdly,
@quakersArmsTradeReport2025


I don't know how much more clearly to put this: we really shouldn't be selling things, especially arms, to nations that are actively committing genocide.
That's crazy behaviour.

#pagebreak()
#bibliography(
  "references.bib",
  title: [References],
  style: "iso-690-numeric",
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
== Government statistics
The Australian Government's arms trade, and indeed military dealings, has been called some of the most secretive in the world. // TODO: citation
For example, Australian export has long
Indeed, Freedom of Information (FOI) requests are one of the primary methods in which real detailed information regarding Australian arms exports have been obtained.
The existing mechanisms are not so useful.


This section examines all of the sources of Government data on arms trade.

=== Defence Export Controls
The Defence Export Controls (DEC) is a Defence body that issues permits for Australian arms exports.
The list of items under control are described in the Defence and Strategic Goods List (DSGL).
The DSGL includes items like body armour and bombs, but also the software and technology associated with any item in the list.
Additionally, dual-use goods, which are items with both commercial and military application such as electronics and avionics, are included on the DSGL.
Ultimately, discretion is with the Defence Minister to determine if an export is in breach of Australia treaty obligations.
#footnote[
  Fun fact, technically there is no limit to the Defence Minister's power here.
  Because the DSGL cannot be exhaustive, the Defence Minister has the ability to determine that #emph[any] export is an arms export and therefore prevent it. // TODO: source?
]

With warhawks defining the Department of Defence's reporting as "nonsensical" @hellyerDefenceMurkyExport2025.

It is important to note that DEC's primary data relates to the application for export permits made by companies, not the exports themselves.
In other words, the data is more about the paperwork being filed for requests to be able to export to DEC rather than actual sales.
However, DEC data may serve as a useful measure of trade activity within the Australian arms export world.


The 2024 figure of \$100 billion is unlikely to mean that literally \$100 billion worth of exports were made.

In 2025 DEC began releasing more detailed geographical information about export location.
DEC data stated exports according to continent, which is largely useless.

=== The Australian Bureau of Statistics
The Australian Bureau of Statistics (ABS) maintains datasets on trade exports @absTradeStatistics2025, including arms and ammunition.

=== Department of Foreign Affairs and Trade
The Department of Foreign Affairs and Trade (DFAT) is responsible for developing Australian's international interests, including foreign policy and international trade.
The arms trade is tied to Australia's "security" interests.

It has been noted by a few places that the Department of Foreign Affairs and Trade (DFAT) have defence numbers that differ to the ABS.

This has been interpreted by various organisations as the result of failures for transparency.
While it is absolutely true that Australia's arms trade lacks transparency, I have found that this is not the reason DFAT and ABS numbers differ.

Parallel to this, the Department of Foreign Affairs and Trade (DFAT) maintains its own trade data of arms and ammunition (#ref(<fig-economic-statistics>)a).

#figure(
  image("images/abs_dfat_comparison.png"),
  caption: [
    Export values
    #pl[a] Export statistics from the ABS and DFAT.
    DFAT values are derived from ABS values, but have "minor" adjustments and are recategorised.
    Orange, difference between ABS and DFAT data.
    #pl[b] The difference between DFAT and ABS values are explained by exclusion of Armoured Fighting Vehicles (AFVs) from DFAT's figures.
    Orange bars, ABS - DFAT values also reflected in a.
    #pl[c] Remaining difference between DFAT figures after ATVs are added.
    #figsource[ABS and DFAT]
  ],
)<fig-economic-statistics>



==== The differences in DFAT and ABS statistics explained
Many analysts have noted that DFAT and ABS have different values for their arms export figures, and interpreted this as a lack of transparency.
I have identified the origin of this apparent discrepancy.

DFAT's arms exports values are consistently lower than compared to ABS figures.
I have found that this is because ABS categorises exports according to Standard International Trade Classification (SITC) while DFAT uses the Australian Harmonised Export Commodity Classification (AHECC).
The key difference is that armoured fighting vehicles are included in the SITC's arms and weapons category (891) while AHECC's arms and weapons category (93) does not include vehicles (87).
The proof is found when DFAT's arms and weapons values are added to the vehicles values, as they are very close matches for the ABS values (#ref(<fig-economic-statistics>)b).
Between 2007 and 2024 DFAT and ABS values differ by a total of \$707 million, and across the same time AFVs totalled \$713 million.

After accounting for AFVs, ABS and DFAT values can still differ by up to \$2 million (#ref(<fig-economic-statistics>)c).

These millions may be the  result of other (smaller) differences in categorisation, as well as corrections (including changing inaccurately coded materials) that DFAT makes to the data derived from ABS.
This may be because AHECC has other differences to SITC.
Ultimately, because DFAT's data is derived from ABS data there is no (data-related) reason to suppose that analysing DFAT data will provide additional insights.
The fact that after adding AFVs into DFAT's arms and ammuntion values there are sometimes millions leftover suggests that DFAT's data is more than just ABS' with AFV subtracted and minor corrections, but other categories at play.
It is for this reason that further analysis of export data utilises only ABS data.
However, it is important to note that neither AHECC nor SITC categories include servicing, which forms a large bulk of Australia's arms export industry.

However, I will maintain the dataset because it may be a useful

=== The Defence Industry Account
A relatively new source of data on the arms industry in Australia is ABS's Australian Defence Industry Account (ADIA), which uses invoices from a supplier of a goods or service to the Department of Defence @absDefenceIndustryAccount2024.
Therefore, this data does not include overseas expenses.
