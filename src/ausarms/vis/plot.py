
from matplotlib import ticker
from matplotlib.axes import Axes
import pandas as pd
import seaborn as sns

from ausarms.vis import palette

aud_to_usd = 0.6734 # Average exchange rate financial year to July 2023
usd_to_aud = 1 / aud_to_usd

def plot_milex(ax: Axes, measure_type: str, aus_data: pd.DataFrame, global_data: pd.DataFrame) -> None:
    if measure_type == 'share_of_gov_spending':
        ylabel = None
        title = 'Military Expenditure as\nShare of Government Spending'
    if measure_type == 'per_capita':
        ylabel = 'AUD'
        title = 'Military Expenditure\nper capita'


    if measure_type == 'per_capita':
        aus_data['expenditure'] = aus_data['expenditure'] * usd_to_aud
        global_data['expenditure'] = global_data['expenditure'] * usd_to_aud


    if measure_type == 'share_of_gov_spending':
        # set ticks to have percents
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(1, decimals=0))
    elif measure_type == 'per_capita':
        # add dollar sign to ticks
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))

    ax.plot(aus_data.year, aus_data.expenditure, label='Australia', color=palette.rgb('Australia'))
    sns.despine(ax=ax, left=True, offset=5)

    ax.set_xlabel('Year')
    ax.set_title(title)

    data = global_data.groupby('year').expenditure
    average = data.median().values
    # err = data.std()
    # mad_per_year = data.apply(
    #         lambda x: (x - x.median()).abs().median()
    #     )
    # err = mad_per_year
    ax.plot(data.mean().index, average, linestyle='-', color='grey', linewidth=1, label='Global median')
    # ax.fill_between(data.mean().index, average - err, average + err,
    #                 alpha=0.3, color='grey', edgecolor='none',
    #                 label='Global median')
    ax.set_location((1.5, 1.5, 10, 5), method='size')
    ax.set_ylim(0, None)
    ax.set_ylabel(ylabel)
    legend = ax.legend()
    legend.set_frame_on(False)

def calculate_decade_mean(yearly_total: pd.Series) -> tuple[list[int], list[float]]:
    years = [year for year in range(1950, 2011, 10)]
    year_data = []
    for year in years:
        decade = yearly_total[(yearly_total.index >= year) & (yearly_total.index < year + 10)].sum() / 10
        year_data.append(decade)
    return years, year_data

def plot_transfer(ax: Axes, data: pd.Series) -> None:
    ax.bar(data.index, data.values, color=palette.rgb('Australia'), width=1, label='Yearly total')
    x, y = calculate_decade_mean(data)
    ax.plot([year + 5 for year in x], y, label='Decade average', 
            linewidth=1,
            color='r', marker='s', markerfacecolor='none',
    )

    ax.set_ylabel('Arms Volume\n(Trend Indicator Value)')
    sns.despine(ax=ax, left=False, offset=5)
    ax.set_xlabel('Year')

def plot_weapon_distribution(ax: Axes, transferdata: pd.DataFrame) -> None:
    data = transferdata.groupby('weapon_description').tiv_total_order.sum()
    data.index = [label[0].upper() + label[1:] for label in data.index]
    data.sort_values(ascending=False, inplace=True)
    ax.barh(data.index, data.values / data.values.sum() * 100, color=palette.rgb('Australia'))
    sns.despine(ax=ax, left=True)
    ax.set_ylim(-1, len(data) + 1)
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(100, decimals=0))

def plot_order_data(ax: Axes, df: pd.DataFrame) -> None:
    data = df.iloc[:-1].groupby('year_ordered').id.count()
    ax.bar(data.index, data.values, width=0.8, color=palette.rgb('Australia'))
    ax.set_xlabel('Year')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    sns.despine(ax=ax, left=True, offset=5)

def plot_category_data(ax: Axes, df: pd.DataFrame) -> None:
    data = df.groupby('category').id.count()
    data.sort_values(ascending=False, inplace=True)
    ax.barh(data.index, data.values / data.values.sum() * 100, color=palette.rgb('Australia'))
    ax.set_ylim(-.5, len(data))
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(100, decimals=0))
    sns.despine(ax=ax, left=True, offset=5)