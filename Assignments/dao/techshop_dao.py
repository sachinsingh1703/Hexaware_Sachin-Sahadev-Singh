from abc import ABC, abstractmethod
from typing import List, Optional
from entity.model.entities import Customer, Product, Order, OrderDetail, Inventory
from util.db_connection import DBConnUtil
from decimal import Decimal
from datetime import datetime
from exception.techshop_exceptions import (
    DatabaseConnectionError,
    CustomerNotFoundError,
    ProductNotFoundError,
    OrderNotFoundError,
    InsufficientStockError,
    InvalidDataError,
    OrderProcessingError
)

class TechShopDAO(ABC):
    @abstractmethod
    def add_customer(self, customer: Customer) -> bool:
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def update_customer(self, customer: Customer) -> bool:
        pass

    @abstractmethod
    def add_product(self, product: Product) -> bool:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> bool:
        pass

    @abstractmethod
    def create_order(self, order: Order) -> bool:
        pass

    @abstractmethod
    def add_order_detail(self, order_detail: OrderDetail) -> bool:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def update_inventory(self, inventory: Inventory) -> bool:
        pass

    @abstractmethod
    def get_inventory_by_product(self, product_id: int) -> Optional[Inventory]:
        pass

    @abstractmethod
    def get_all_customers(self) -> List[Customer]:
        pass

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    def get_all_order_details(self) -> List[OrderDetail]:
        pass

    @abstractmethod
    def get_all_inventory(self) -> List[Inventory]:
        pass

class TechShopDAOImpl(TechShopDAO):
    def __init__(self):
        self.conn = None

    def _get_connection(self):
        try:
            if not self.conn:
                self.conn = DBConnUtil.get_connection()
            return self.conn
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}")

    def add_customer(self, customer: Customer) -> bool:
        try:
            if not all([customer.first_name, customer.last_name, customer.email]):
                raise InvalidDataError("Required customer fields are missing")
            
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO Customers (FirstName, LastName, Email, Phone, Address)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                customer.first_name,
                customer.last_name,
                customer.email,
                customer.phone,
                customer.address
            ))
            conn.commit()
            return True
        except InvalidDataError:
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error adding customer: {str(e)}")

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT CustomerID, FirstName, LastName, Email, Phone, Address
            FROM Customers
            WHERE CustomerID = ?
            """
            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()
            if row:
                return Customer(
                    customer_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    phone=row[4],
                    address=row[5]
                )
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
        except CustomerNotFoundError:
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving customer: {str(e)}")

    def update_customer(self, customer: Customer) -> bool:
        try:
            if not customer.customer_id:
                raise InvalidDataError("Customer ID is required for update")
            
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            UPDATE Customers 
            SET FirstName = ?, LastName = ?, Email = ?, Phone = ?, Address = ?
            WHERE CustomerID = ?
            """
            cursor.execute(query, (
                customer.first_name,
                customer.last_name,
                customer.email,
                customer.phone,
                customer.address,
                customer.customer_id
            ))
            if cursor.rowcount == 0:
                raise CustomerNotFoundError(f"Customer with ID {customer.customer_id} not found")
            conn.commit()
            return True
        except (InvalidDataError, CustomerNotFoundError):
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error updating customer: {str(e)}")

    def add_product(self, product: Product) -> bool:
        try:
            if not all([product.product_name, product.price]):
                raise InvalidDataError("Product name and price are required")
            if product.price <= 0:
                raise InvalidDataError("Product price must be greater than 0")
            
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO Products (ProductName, Description, Price)
            VALUES (?, ?, ?)
            """
            cursor.execute(query, (
                product.product_name,
                product.description,
                float(product.price)
            ))
            conn.commit()
            return True
        except InvalidDataError:
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error adding product: {str(e)}")

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT ProductID, ProductName, Description, Price
            FROM Products
            WHERE ProductID = ?
            """
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()
            if row:
                return Product(
                    product_id=row[0],
                    product_name=row[1],
                    description=row[2],
                    price=Decimal(str(row[3]))
                )
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving product: {str(e)}")

    def update_product(self, product: Product) -> bool:
        try:
            if not product.product_id:
                raise InvalidDataError("Product ID is required for update")
            if product.price <= 0:
                raise InvalidDataError("Product price must be greater than 0")
            
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            UPDATE Products 
            SET ProductName = ?, Description = ?, Price = ?
            WHERE ProductID = ?
            """
            cursor.execute(query, (
                product.product_name,
                product.description,
                float(product.price),
                product.product_id
            ))
            if cursor.rowcount == 0:
                raise ProductNotFoundError(f"Product with ID {product.product_id} not found")
            conn.commit()
            return True
        except (InvalidDataError, ProductNotFoundError):
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error updating product: {str(e)}")

    def create_order(self, order: Order) -> bool:
        try:
            if not order.customer_id:
                raise InvalidDataError("Customer ID is required for order")
            if order.total_amount <= 0:
                raise InvalidDataError("Order total amount must be greater than 0")
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verify customer exists
            customer_query = "SELECT CustomerID FROM Customers WHERE CustomerID = ?"
            cursor.execute(customer_query, (order.customer_id,))
            if not cursor.fetchone():
                raise CustomerNotFoundError(f"Customer with ID {order.customer_id} not found")
            
            query = """
            INSERT INTO Orders (CustomerID, OrderDate, TotalAmount)
            VALUES (?, ?, ?)
            """
            cursor.execute(query, (
                order.customer_id,
                order.order_date,
                float(order.total_amount)
            ))
            conn.commit()
            return True
        except (InvalidDataError, CustomerNotFoundError):
            raise
        except Exception as e:
            raise OrderProcessingError(f"Error creating order: {str(e)}")

    def add_order_detail(self, order_detail: OrderDetail) -> bool:
        try:
            if not all([order_detail.order_id, order_detail.product_id, order_detail.quantity]):
                raise InvalidDataError("Order ID, Product ID and quantity are required")
            if order_detail.quantity <= 0:
                raise InvalidDataError("Order quantity must be greater than 0")
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if product exists and has sufficient stock
            inventory_query = """
            SELECT QuantityInStock 
            FROM Inventory 
            WHERE ProductID = ?
            """
            cursor.execute(inventory_query, (order_detail.product_id,))
            inventory_row = cursor.fetchone()
            if not inventory_row:
                raise ProductNotFoundError(f"Product with ID {order_detail.product_id} not found in inventory")
            if inventory_row[0] < order_detail.quantity:
                raise InsufficientStockError(f"Insufficient stock for product ID {order_detail.product_id}")
            
            query = """
            INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
            VALUES (?, ?, ?)
            """
            cursor.execute(query, (
                order_detail.order_id,
                order_detail.product_id,
                order_detail.quantity
            ))
            
            # Update inventory
            update_inventory_query = """
            UPDATE Inventory 
            SET QuantityInStock = QuantityInStock - ?
            WHERE ProductID = ?
            """
            cursor.execute(update_inventory_query, (
                order_detail.quantity,
                order_detail.product_id
            ))
            
            conn.commit()
            return True
        except (InvalidDataError, ProductNotFoundError, InsufficientStockError):
            raise
        except Exception as e:
            raise OrderProcessingError(f"Error adding order detail: {str(e)}")

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT OrderID, CustomerID, OrderDate, TotalAmount
            FROM Orders
            WHERE OrderID = ?
            """
            cursor.execute(query, (order_id,))
            row = cursor.fetchone()
            if row:
                return Order(
                    order_id=row[0],
                    customer_id=row[1],
                    order_date=row[2],
                    total_amount=Decimal(str(row[3]))
                )
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        except OrderNotFoundError:
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving order: {str(e)}")

    def update_inventory(self, inventory: Inventory) -> bool:
        try:
            if not inventory.product_id:
                raise InvalidDataError("Product ID is required for inventory update")
            if inventory.quantity_in_stock < 0:
                raise InvalidDataError("Quantity in stock cannot be negative")
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verify product exists
            product_query = "SELECT ProductID FROM Products WHERE ProductID = ?"
            cursor.execute(product_query, (inventory.product_id,))
            if not cursor.fetchone():
                raise ProductNotFoundError(f"Product with ID {inventory.product_id} not found")
            
            query = """
            UPDATE Inventory 
            SET QuantityInStock = ?, LastStockUpdate = ?
            WHERE ProductID = ?
            """
            cursor.execute(query, (
                inventory.quantity_in_stock,
                inventory.last_stock_update,
                inventory.product_id
            ))
            if cursor.rowcount == 0:
                # If no rows updated, insert new inventory record
                insert_query = """
                INSERT INTO Inventory (ProductID, QuantityInStock, LastStockUpdate)
                VALUES (?, ?, ?)
                """
                cursor.execute(insert_query, (
                    inventory.product_id,
                    inventory.quantity_in_stock,
                    inventory.last_stock_update
                ))
            conn.commit()
            return True
        except (InvalidDataError, ProductNotFoundError):
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error updating inventory: {str(e)}")

    def get_inventory_by_product(self, product_id: int) -> Optional[Inventory]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT InventoryID, ProductID, QuantityInStock, LastStockUpdate
            FROM Inventory
            WHERE ProductID = ?
            """
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()
            if row:
                return Inventory(
                    inventory_id=row[0],
                    product_id=row[1],
                    quantity_in_stock=row[2],
                    last_stock_update=row[3]
                )
            raise ProductNotFoundError(f"Inventory not found for product ID {product_id}")
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving inventory: {str(e)}")

    def get_all_customers(self) -> List[Customer]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT CustomerID, FirstName, LastName, Email, Phone, Address
            FROM Customers
            ORDER BY CustomerID DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            customers = []
            for row in rows:
                customer = Customer(
                    customer_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    phone=row[4],
                    address=row[5]
                )
                customers.append(customer)
            return customers
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving customers: {str(e)}")

    def get_all_products(self) -> List[Product]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT ProductID, ProductName, Description, Price
            FROM Products
            ORDER BY ProductID DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = Product(
                    product_id=row[0],
                    product_name=row[1],
                    description=row[2],
                    price=Decimal(str(row[3]))
                )
                products.append(product)
            return products
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving products: {str(e)}")

    def get_all_orders(self) -> List[Order]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT OrderID, CustomerID, OrderDate, TotalAmount
            FROM Orders
            ORDER BY OrderID DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                order = Order(
                    order_id=row[0],
                    customer_id=row[1],
                    order_date=row[2],
                    total_amount=Decimal(str(row[3]))
                )
                orders.append(order)
            return orders
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving orders: {str(e)}")

    def get_all_order_details(self) -> List[OrderDetail]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT od.OrderDetailID, od.OrderID, od.ProductID, od.Quantity,
                   p.ProductName, p.Price
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            ORDER BY od.OrderDetailID DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            order_details = []
            for row in rows:
                order_detail = OrderDetail(
                    order_detail_id=row[0],
                    order_id=row[1],
                    product_id=row[2],
                    quantity=row[3],
                    product_name=row[4],  # Additional info from Products table
                    unit_price=Decimal(str(row[5]))  # Additional info from Products table
                )
                order_details.append(order_detail)
            return order_details
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving order details: {str(e)}")

    def get_all_inventory(self) -> List[Inventory]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            SELECT i.InventoryID, i.ProductID, i.QuantityInStock, i.LastStockUpdate,
                   p.ProductName
            FROM Inventory i
            JOIN Products p ON i.ProductID = p.ProductID
            ORDER BY i.InventoryID DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            inventories = []
            for row in rows:
                inventory = Inventory(
                    inventory_id=row[0],
                    product_id=row[1],
                    quantity_in_stock=row[2],
                    last_stock_update=row[3],
                    product_name=row[4]  # Additional info from Products table
                )
                inventories.append(inventory)
            return inventories
        except Exception as e:
            raise DatabaseConnectionError(f"Error retrieving inventory: {str(e)}") 