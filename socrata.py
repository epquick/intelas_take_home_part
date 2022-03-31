import json
import urllib.request
from json import JSONDecodeError
from typing import List
from urllib.error import URLError
import re

from models import RealEstateTransaction


class SocrataTransactionHistoryGrabber:
    API_URL = 'https://data.ct.gov/resource/5mzw-sjtu.json'

    @classmethod
    def grab(cls) -> List[RealEstateTransaction]:
        socrata_data = cls._download_data()
        cls._validate_data(socrata_data)
        return cls._parse_data(socrata_data)

    @classmethod
    def _download_data(cls):
        try:
            with urllib.request.urlopen(cls.API_URL) as response:
                return json.loads(response.read())
        except (URLError, JSONDecodeError) as e:
            raise SocrataError

    @classmethod
    def _validate_data(cls, socrata_data):
        if type(socrata_data) != list:
            raise SocrataError

        for transaction_data in socrata_data:
            cls._validate_transaction_data(transaction_data)

    @classmethod
    def _validate_transaction_data(cls, transaction_data):
        if type(transaction_data) != dict:
            raise SocrataError
        if not (transaction_data.get('town') and transaction_data.get('saleamount') and
                transaction_data.get('salesratio') and transaction_data.get('daterecorded')):
            raise SocrataError
        if not cls._validate_number(transaction_data.get('saleamount')):
            raise SocrataError
        if not cls._validate_number(transaction_data.get('salesratio')):
            raise SocrataError
        if not cls._validate_date(transaction_data.get('daterecorded')):
            raise SocrataError

    @classmethod
    def _validate_number(cls, string):
        return string.replace('.', '', 1).isdigit()

    regex_iso8601 = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex_iso8601).match

    @classmethod
    def _validate_date(cls, string):
        return cls.match_iso8601(string) is not None

    @classmethod
    def _parse_data(cls, socrata_data) -> List[RealEstateTransaction]:
        return [cls._parse_transaction_data(transaction_data) for transaction_data in socrata_data]

    @classmethod
    def _parse_transaction_data(cls, transaction_data) -> RealEstateTransaction:
        return RealEstateTransaction(town_name=transaction_data['town'],
                                     sale_amount=float(transaction_data['saleamount']),
                                     sales_ratio=float(transaction_data['salesratio']),
                                     year=int(transaction_data['daterecorded'][:4]))


class SocrataError(Exception):
    pass
