from decimal import Decimal
from dataclasses import dataclass
from typing import List

from models import RealEstateTransaction


@dataclass
class StatisticsItem:
    year: int = None
    town_name: str = None
    sales_ratio: Decimal = 0
    sales_volume: Decimal = 0


class RealEstateStatisticsAccumulator:
    statistics: {int: {str: StatisticsItem}} = {}  # {year: {town_name: StatisticsItem}}

    #################################
    # Statistics collecting functions

    def add_transactions(self, transactions: List[RealEstateTransaction]):
        for transaction in transactions:
            self.add_one_transaction(transaction)

    def add_one_transaction(self, transaction: RealEstateTransaction):
        statistics_item = self._get_statistics_item(transaction.year, transaction.town_name)

        self._obtain_sales_ratio(statistics_item, transaction)
        self._obtain_sales_valume(statistics_item, transaction)

    def _get_statistics_item(self, year: int, town_name: str) -> StatisticsItem:
        if year not in self.statistics:
            self.statistics[year] = {}
        if town_name not in self.statistics[year]:
            self.statistics[year][town_name] = StatisticsItem(year=year, town_name=town_name)
        return self.statistics[year][town_name]

    def _obtain_sales_ratio(self, statistics_item: StatisticsItem, transaction: RealEstateTransaction):
        statistics_item.sales_ratio = max(statistics_item.sales_ratio, transaction.sales_ratio)

    def _obtain_sales_valume(self, statistics_item: StatisticsItem, transaction: RealEstateTransaction):
        statistics_item.sales_volume += transaction.sale_amount

    #################################
    # Statistics retrieving functions

    def get_available_years(self) -> List[int]:
        return list(self.statistics.keys())

    def get_year_top_by_sales_ratio(self, year: int, number_of_records: int) -> List[StatisticsItem]:
        statistics = self.statistics[year].values()
        statistics = sorted(statistics, key=lambda x: -x.sales_ratio)
        return statistics[:number_of_records]

    def get_year_top_by_sales_volume(self, year: int, number_of_records: int) -> List[StatisticsItem]:
        statistics = self.statistics[year].values()
        statistics = sorted(statistics, key=lambda x: -x.sales_volume)
        return statistics[:number_of_records]


