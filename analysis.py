# %%
import matplotlib as mpl
import pandas as pd
import scilayout
import sqlalchemy as sa

from ausarms import crud, database, vis

engine = database.create_engine("sqlite")  # or "postgresql"
SessionMaker = database.create_session(engine)
session = SessionMaker()
# %%
mpl.rc_file('src/ausarms/vis/ausarms.mplstyle')
fig = scilayout.figure()
# %%

# measure_type = 'share_of_gov_spending'
# measure_type = 'current_usd'
# measure_type = 'share_of_gdp'
# measure_type = 'per_capita'

# TODO: requires postgres
# df_global_median = pd.read_sql(
#     session.query(crud.Expenditure.year, 
#                  sa.func.percentile_cont(0.5).within_group(crud.Expenditure.expenditure.asc()).label('expenditure'))
#     .filter(crud.Expenditure.measure_type == measure_type)
#     .group_by(crud.Expenditure.year)
#     .statement,
#     session.bind
# )

def query_expenditure(session: sa.orm.Session, measure_type: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_aus = pd.read_sql(
            session.query(crud.Expenditure).join(crud.Country)
            .filter(crud.Country.name == 'Australia', crud.Expenditure.measure_type == measure_type)
            .statement,
            session.bind
        )

    df_global = pd.read_sql(
        session.query(crud.Expenditure)
        .filter(crud.Expenditure.measure_type == measure_type)
        .statement,
        session.bind
    )

    return df_aus, df_global

# fig = scilayout.figure()
fig.clear()
ax_gov = fig.add_panel((1.5, 1.5, 10, 5), method='size')
ax_capita = fig.add_panel((1.5, 1.5, 10, 5), method='size')
vis.plot.plot_milex(ax_gov, 'share_of_gov_spending', *query_expenditure(session, 'share_of_gov_spending'))
vis.plot.plot_milex(ax_capita, 'per_capita', *query_expenditure(session, 'per_capita'))

fig.set_size_cm(21, 15)
width, height = 7, 5
ax_gov.set_location((1.5, 1.5, width, height), method='size')
ax_gov.add_label('a')
ax_capita.set_location((11, 1.5, width, height), method='size')
ax_capita.legend().remove()
ax_capita.add_label('b')
# %%
filename = f"images/milex_australia.svg"
fig.export(filename)
# %% Transfer data
# query the table and inert country names into the table
# df_transfers = pd.read_sql(
#     # session.query(crud.Transfer).join(crud.Country, crud.Transfer.supplier == crud.Country.id)
#     session.query(crud.Transfer).join(crud.Country, crud.Transfer.supplier == crud.Country.id)
#     .add_columns(crud.Country.name.label('country_name'))
#     .statement,
#     session.bind
# )
# Create aliases for the Country table to join it twice
supplier_country = sa.orm.aliased(crud.Country)
recipient_country = sa.orm.aliased(crud.Country)

query = session.query(crud.Transfer)

# Add country names to the table for extraction
query = query.join(supplier_country, crud.Transfer.supplier == supplier_country.id)
query = query.join(recipient_country, crud.Transfer.recipient == recipient_country.id)
query_core = query.add_columns(
    supplier_country.name.label('supplier_name'),
    recipient_country.name.label('recipient_name')
)

# Could equally do this with pandas, but I this is more about the SQL
query = query_core.join(crud.Country, crud.Transfer.supplier == crud.Country.id).filter(crud.Country.name == 'Australia')
df_supplier = pd.read_sql(
    query.statement,
    session.bind
)

query = query_core.join(crud.Country, crud.Transfer.recipient == crud.Country.id).filter(crud.Country.name == 'Australia')
df_recipient = pd.read_sql(
    query.statement,
    session.bind
)
# %%
fig.clear()


ax_exports = fig.add_panel((2, 1.5, 10, 5), method='size')
ax_exports.add_label('a')
# ax_imports = fig.add_panel((14.5, 1.5, 6, 5), method='size')
# ax_imports.add_label('b')
ax_export_dist = fig.add_panel((2, 7.5, 18.5, 6), method='size')
ax_export_dist.add_label('b')

# incoming = df_recipient.groupby('year_ordered').tiv_total_order.sum()
outgoing = df_supplier.groupby('year_ordered').tiv_total_order.sum()
# plot_transfer(ax_imports, incoming)
vis.plot.plot_transfer(ax_exports, outgoing)
vis.plot.plot_weapon_distribution(ax_export_dist, df_supplier)
# ax_imports.set_title('Arms Import Volume')
ax_exports.set_title('Arms Export Volume')

legend = ax_exports.legend()
legend.set_frame_on(False)
# ax_imports.annotate("72\nF-35 jets",
#             xy=(2009, 4000), xytext=(2015, 2800),
#             arrowprops=dict(arrowstyle='->', color='grey'))
# ax_imports.annotate("3 ships and\n24 F-18 jets",
#             xy=(2007, 4000), xytext=(1980, 2800),
#             arrowprops=dict(arrowstyle='->', color='grey'))
ax_exports.annotate("15 transport\nships",
            xy=(2009, 520), xytext=(1975, 400),
            arrowprops=dict(arrowstyle='->', color='grey'))
ax_exports.annotate("600\nmissiles",
            xy=(1970, 406), xytext=(1949, 300),
            arrowprops=dict(arrowstyle='->', color='grey'))

# link x axis between them
# for ax in [ax_imports, ax_exports]:
    # ax.set_xlim(1943, 2026)


fig.set_size_cm(21, 10)
ax_exports.set_location((2, 1, 5, 7), method='size')
ax_export_dist.set_location((12, 0, 7, 8.5), method='size')
ax_export_dist.panellabel.set_offset(y=0.9, x=-4.5)
ax_export_dist.set_title('Export type', y=0.88)
# %%
fig.export('images/transfer_australia.svg')

# %%

query = session.query(crud.Export)
df_cod = pd.read_sql(query.statement, session.bind)

# %%



mpl.rc_file('src/ausarms/vis/ausarms.mplstyle')
fig.clear()
ax_orders = fig.add_panel((2, 1.5, 5, 5), method='size')
ax_categories = fig.add_panel((10, 1.5, 5, 5), method='size')
vis.plot.plot_order_data(ax_orders, df_cod)
vis.plot.plot_category_data(ax_categories, df_cod)

# %%
ax_orders.set_location((2, 1.5, 7, 5), method='size')
ax_orders.add_label('a')
ax_orders.set_title("Australian arms exports")
ax_orders.set_ylabel('# of exports')
ax_categories.set_location((14, 1.5, 3, 5), method='size')
ax_categories.set_title("Export categories")
ax_categories.add_label('b')
# %%
fig.export('images/cod_data.svg')

session.close()