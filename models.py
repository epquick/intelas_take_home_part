from dataclasses import dataclass


@dataclass
class RealEstateTransaction:
    town_name: str = None
    sales_ratio: float = None
    sale_amount: float = None
    year: int = None

