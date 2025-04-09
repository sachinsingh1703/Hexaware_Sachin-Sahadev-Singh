from database_connector import DatabaseConnector
from exceptions import InvalidDataException, InsufficientStockException, IncompleteOrderException
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from customer import Customer
from product import Product

class OrderDetail:
    def __init__(self, order_id: int, product: Product, quantity: int, 
                 unit_price: Decimal = None, discount: Decimal = Decimal('0.00'),
                 order_detail_id: int = None):
        self._order_detail_id = order_detail_id
        self._order_id = order_id
        self._product = product
        self._quantity = None
        self._unit_price = None
        self._discount = None

        # Set values using properties to ensure validation
        self.quantity = quantity
        self.unit_price = unit_price if unit_price is not None else product.price
        self.discount = discount

        self._db = DatabaseConnector()

    @property
    def order_detail_id(self) -> int:
        return self._order_detail_id

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise InvalidDataException("Quantity must be a positive integer")
        self._quantity = value

    @property
    def unit_price(self) -> Decimal:
        return self._unit_price

    @unit_price.setter
    def unit_price(self, value: Decimal):
        if not isinstance(value, (int, float, Decimal)):
            raise InvalidDataException("Unit price must be a numeric value")
        value = Decimal(str(value))
        if value < 0:
            raise InvalidDataException("Unit price cannot be negative")
        self._unit_price = value

    @property
    def discount(self) -> Decimal:
        return self._discount

    @discount.setter
    def discount(self, value: Decimal):
        if not isinstance(value, (int, float, Decimal)):
            raise InvalidDataException("Discount must be a numeric value")
        value = Decimal(str(value))
        if value < 0 or value > 100:
            raise InvalidDataException("Discount must be between 0 and 100")
        self._discount = value

    def calculate_subtotal(self) -> Decimal:
        """Calculate the subtotal for this order detail."""
        subtotal = self.quantity * self.unit_price
        if self.discount > 0:
            discount_amount = subtotal * (self.discount / Decimal('100.00'))
            subtotal -= discount_amount
        return subtotal

    def save(self) -> bool:
        """Save or update order detail information in the database."""
        try:
            if self._order_detail_id:
                # Update existing order detail
                query = """
                UPDATE OrderDetails 
                SET OrderID = ?, ProductID = ?, Quantity = ?, 
                    UnitPrice = ?, Discount = ?
                WHERE OrderDetailID = ?
                """
                params = (self.order_id, self.product.product_id, self.quantity,
                         float(self.unit_price), float(self.discount),
                         self._order_detail_id)
            else:
                # Insert new order detail
                query = """
                INSERT INTO OrderDetails (OrderID, ProductID, Quantity, 
                                       UnitPrice, Discount)
                VALUES (?, ?, ?, ?, ?);
                SELECT SCOPE_IDENTITY();
                """
                params = (self.order_id, self.product.product_id, self.quantity,
                         float(self.unit_price), float(self.discount))

            cursor = self._db.execute_query(query, params)
            if not self._order_detail_id:
                self._order_detail_id = int(cursor.fetchone()[0])
            self._db.commit()
            return True
        except Exception as e:
            print(f"Error saving order detail: {str(e)}")
            return False

    def get_order_detail_info(self) -> dict:
        """Retrieve information about this order detail."""
        return {
            'order_detail_id': self._order_detail_id,
            'order_id': self.order_id,
            'product': self.product.get_product_details(),
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'discount': float(self.discount),
            'subtotal': float(self.calculate_subtotal())
        }

    def update_quantity(self, new_quantity: int) -> bool:
        """Update the quantity of the product in this order detail."""
        try:
            self.quantity = new_quantity
            return self.save()
        except Exception as e:
            print(f"Error updating quantity: {str(e)}")
            return False

    def add_discount(self, discount_percentage: Decimal) -> bool:
        """Apply a discount to this order detail."""
        try:
            self.discount = discount_percentage
            return self.save()
        except Exception as e:
            print(f"Error applying discount: {str(e)}")
            return False

class Order:
    def __init__(self, customer: Customer, order_date: datetime = None, 
                 order_id: int = None):
        self._order_id = order_id
        self._customer = customer
        self._order_date = order_date or datetime.now()
        self._order_details: List[OrderDetail] = []
        self._status = "Processing"
        self._db = DatabaseConnector()

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def order_date(self) -> datetime:
        return self._order_date

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        valid_statuses = ["Processing", "Shipped", "Delivered", "Cancelled"]
        if value not in valid_statuses:
            raise InvalidDataException(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        self._status = value

    def add_order_detail(self, product: Product, quantity: int, 
                        unit_price: Decimal = None, discount: Decimal = Decimal('0.00')) -> bool:
        """Add a new order detail to this order."""
        if not self._order_id:
            raise IncompleteOrderException("Order must be saved before adding details")

        # Check if product is in stock
        if not product.is_product_in_stock():
            raise InsufficientStockException(f"Product {product.product_name} is out of stock")

        order_detail = OrderDetail(
            order_id=self._order_id,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            discount=discount
        )
        
        if order_detail.save():
            self._order_details.append(order_detail)
            return True
        return False

    def calculate_total_amount(self) -> Decimal:
        """Calculate the total amount of the order."""
        return sum(detail.calculate_subtotal() for detail in self._order_details)

    def save(self) -> bool:
        """Save or update order information in the database."""
        try:
            if self._order_id:
                # Update existing order
                query = """
                UPDATE Orders 
                SET CustomerID = ?, OrderDate = ?, TotalAmount = ?,
                    OrderStatus = ?
                WHERE OrderID = ?
                """
                params = (self.customer.customer_id, self.order_date,
                         float(self.calculate_total_amount()), self.status,
                         self._order_id)
            else:
                # Insert new order
                query = """
                INSERT INTO Orders (CustomerID, OrderDate, TotalAmount, OrderStatus)
                VALUES (?, ?, ?, ?);
                SELECT SCOPE_IDENTITY();
                """
                params = (self.customer.customer_id, self.order_date,
                         float(self.calculate_total_amount()), self.status)

            cursor = self._db.execute_query(query, params)
            if not self._order_id:
                self._order_id = int(cursor.fetchone()[0])
            self._db.commit()
            return True
        except Exception as e:
            print(f"Error saving order: {str(e)}")
            return False

    def get_order_details(self) -> dict:
        """Retrieve the details of the order."""
        return {
            'order_id': self._order_id,
            'customer': self.customer.get_customer_details(),
            'order_date': self.order_date.isoformat(),
            'status': self.status,
            'total_amount': float(self.calculate_total_amount()),
            'order_details': [detail.get_order_detail_info() 
                            for detail in self._order_details]
        }

    def update_order_status(self, new_status: str) -> bool:
        """Update the status of the order."""
        try:
            self.status = new_status
            return self.save()
        except Exception as e:
            print(f"Error updating order status: {str(e)}")
            return False

    def cancel_order(self) -> bool:
        """Cancel the order and adjust stock levels."""
        try:
            if self.status == "Cancelled":
                return True
            
            self.status = "Cancelled"
            return self.save()
        except Exception as e:
            print(f"Error cancelling order: {str(e)}")
            return False

    @classmethod
    def get_by_id(cls, order_id: int) -> Optional['Order']:
        """Retrieve an order by its ID."""
        db = DatabaseConnector()
        try:
            # Get order information
            query = """
            SELECT OrderID, CustomerID, OrderDate, OrderStatus
            FROM Orders
            WHERE OrderID = ?
            """
            cursor = db.execute_query(query, (order_id,))
            row = cursor.fetchone()
            
            if not row:
                return None

            # Get customer
            customer = Customer.get_by_id(row[1])
            if not customer:
                return None

            # Create order instance
            order = cls(
                customer=customer,
                order_date=row[2],
                order_id=row[0]
            )
            order.status = row[3]

            # Get order details
            details_query = """
            SELECT od.OrderDetailID, od.ProductID, od.Quantity, 
                   od.UnitPrice, od.Discount
            FROM OrderDetails od
            WHERE od.OrderID = ?
            """
            cursor = db.execute_query(details_query, (order_id,))
            
            for detail_row in cursor.fetchall():
                product = Product.get_by_id(detail_row[1])
                if product:
                    order_detail = OrderDetail(
                        order_id=order_id,
                        product=product,
                        quantity=detail_row[2],
                        unit_price=Decimal(str(detail_row[3])),
                        discount=Decimal(str(detail_row[4])),
                        order_detail_id=detail_row[0]
                    )
                    order._order_details.append(order_detail)

            return order
        except Exception as e:
            print(f"Error retrieving order: {str(e)}")
            return None
        finally:
            db.close_connection() 