from socrata import SocrataAPI
from statistics_accumulator import RealEstateStatisticsAccumulator


if __name__ == '__main__':
    transactions = SocrataAPI.get_transactions_history()

    statistics = RealEstateStatisticsAccumulator()
    statistics.add_transactions(transactions)

    years = statistics.get_available_years()
    for year in years:
        top_towns_by_sales_ratio = statistics.get_year_top_by_sales_ratio(year, 10)
        top_towns_by_sales_volume = statistics.get_year_top_by_sales_volume(year, 10)

        print('###', year)
        print('Top 10 towns by sales ratio:  ', ', '.join([t.town_name for t in top_towns_by_sales_ratio]))
        print('Top 10 towns by sales volume: ', ', '.join([t.town_name for t in top_towns_by_sales_volume]))
