from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RealEstateTransaction:
    year: int
    town_name: str
    sales_ratio: float
    sale_amount: Decimal

