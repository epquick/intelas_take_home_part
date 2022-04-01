from socrata import SocrataTransactionHistoryGrabber
from statistics import RealEstateStatisticsAccumulator


if __name__ == '__main__':
    transactions_list = SocrataTransactionHistoryGrabber.grab()

    statistics = RealEstateStatisticsAccumulator()
    statistics.add_transactions(transactions_list)

    years = statistics.get_available_years()
    for year in years:
        top_towns_by_sales_ratio = statistics.get_year_top_by_sales_ratio(year, 10)
        top_towns_by_sales_amount = statistics.get_year_top_by_sales_amount(year, 10)

        print('###', year)
        print('Top 10 towns by sales ratio:  ', ', '.join([t.town_name for t in top_towns_by_sales_ratio]))
        print('Top 10 towns by sales amount: ', ', '.join([t.town_name for t in top_towns_by_sales_amount]))
