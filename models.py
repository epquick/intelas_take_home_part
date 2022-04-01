from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RealEstateTransaction:
    town_name: str = None
    sales_ratio: Decimal = None
    sale_amount: Decimal = None
    year: int = None

