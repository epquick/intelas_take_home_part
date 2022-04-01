from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RealEstateTransaction:
    year: int = None
    town_name: str = None
    sales_ratio: Decimal = None
    sale_amount: Decimal = None

