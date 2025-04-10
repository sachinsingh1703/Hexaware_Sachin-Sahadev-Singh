from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Customer:
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    customer_id: Optional[int] = None

@dataclass
class Product:
    product_name: str
    description: str
    price: Decimal
    product_id: Optional[int] = None

@dataclass
class Order:
    customer_id: int
    order_date: datetime
    total_amount: Decimal
    order_id: Optional[int] = None

@dataclass
class OrderDetail:
    order_id: int
    product_id: int
    quantity: int
    order_detail_id: Optional[int] = None

@dataclass
class Inventory:
    product_id: int
    quantity_in_stock: int
    last_stock_update: datetime
    inventory_id: Optional[int] = None 