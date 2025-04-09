from database_connector import DatabaseConnector
from exceptions import InvalidDataException, InsufficientStockException
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from product import Product

class Inventory:
    def __init__(self, product: Product, quantity_in_stock: int = 0, 
                 last_stock_update: datetime = None, inventory_id: int = None):
        self._inventory_id = inventory_id
        self._product = product
        self._quantity_in_stock = None
        self._last_stock_update = last_stock_update or datetime.now()

        # Set values using properties to ensure validation
        self.quantity_in_stock = quantity_in_stock
        
        self._db = DatabaseConnector()

    @property
    def inventory_id(self) -> int:
        return self._inventory_id

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity_in_stock(self) -> int:
        return self._quantity_in_stock

    @quantity_in_stock.setter
    def quantity_in_stock(self, value: int):
        if not isinstance(value, int):
            raise InvalidDataException("Quantity must be an integer")
        if value < 0:
            raise InvalidDataException("Quantity cannot be negative")
        self._quantity_in_stock = value

    @property
    def last_stock_update(self) -> datetime:
        return self._last_stock_update

    def save(self) -> bool:
        """Save or update inventory information in the database."""
        try:
            self._last_stock_update = datetime.now()
            
            if self._inventory_id:
                # Update existing inventory
                query = """
                UPDATE Inventory 
                SET ProductID = ?, QuantityInStock = ?, LastStockUpdate = ?
                WHERE InventoryID = ?
                """
                params = (self.product.product_id, self.quantity_in_stock,
                         self.last_stock_update, self._inventory_id)
                cursor = self._db.execute_query(query, params)
                if cursor:
                    self._db.commit()
                    return True
            else:
                # Insert new inventory
                insert_query = """
                INSERT INTO Inventory (ProductID, QuantityInStock, LastStockUpdate)
                VALUES (?, ?, ?)
                """
                params = (self.product.product_id, self.quantity_in_stock,
                         self.last_stock_update)
                
                cursor = self._db.execute_query(insert_query, params)
                if cursor:
                    self._db.commit()
                    
                    # Get the inserted ID
                    id_query = "SELECT IDENT_CURRENT('Inventory')"
                    cursor = self._db.execute_query(id_query)
                    if cursor:
                        row = cursor.fetchone()
                        if row:
                            self._inventory_id = int(row[0])
                            return True
            return False
        except Exception as e:
            print(f"Error saving inventory: {str(e)}")
            return False

    def get_product(self) -> Product:
        """Retrieve the product associated with this inventory item."""
        return self.product

    def get_quantity_in_stock(self) -> int:
        """Get the current quantity of the product in stock."""
        return self.quantity_in_stock

    def add_to_inventory(self, quantity: int) -> bool:
        """Add a specified quantity of the product to the inventory."""
        try:
            if quantity <= 0:
                raise InvalidDataException("Quantity to add must be positive")
            self.quantity_in_stock += quantity
            return self.save()
        except Exception as e:
            print(f"Error adding to inventory: {str(e)}")
            return False

    def remove_from_inventory(self, quantity: int) -> bool:
        """Remove a specified quantity of the product from the inventory."""
        try:
            if quantity <= 0:
                raise InvalidDataException("Quantity to remove must be positive")
            if quantity > self.quantity_in_stock:
                raise InsufficientStockException("Insufficient stock available")
            self.quantity_in_stock -= quantity
            return self.save()
        except Exception as e:
            print(f"Error removing from inventory: {str(e)}")
            return False

    def update_stock_quantity(self, new_quantity: int) -> bool:
        """Update the stock quantity to a new value."""
        try:
            self.quantity_in_stock = new_quantity
            return self.save()
        except Exception as e:
            print(f"Error updating stock quantity: {str(e)}")
            return False

    def is_product_available(self, quantity_to_check: int) -> bool:
        """Check if a specified quantity of the product is available."""
        return self.quantity_in_stock >= quantity_to_check

    def get_inventory_value(self) -> Decimal:
        """Calculate the total value of the products in the inventory."""
        return self.quantity_in_stock * self.product.price

    @classmethod
    def get_by_product_id(cls, product_id: int) -> Optional['Inventory']:
        """Retrieve inventory information for a specific product."""
        db = DatabaseConnector()
        try:
            query = """
            SELECT i.InventoryID, i.QuantityInStock, i.LastStockUpdate
            FROM Inventory i
            WHERE i.ProductID = ?
            """
            cursor = db.execute_query(query, (product_id,))
            row = cursor.fetchone()
            
            if row:
                product = Product.get_by_id(product_id)
                if product:
                    return cls(
                        inventory_id=row[0],
                        product=product,
                        quantity_in_stock=row[1],
                        last_stock_update=row[2]
                    )
            return None
        except Exception as e:
            print(f"Error retrieving inventory: {str(e)}")
            return None
        finally:
            db.close_connection()

    @classmethod
    def list_low_stock_products(cls, threshold: int) -> List['Inventory']:
        """List products with quantities below a specified threshold."""
        db = DatabaseConnector()
        try:
            query = """
            SELECT i.InventoryID, i.ProductID, i.QuantityInStock, i.LastStockUpdate
            FROM Inventory i
            WHERE i.QuantityInStock < ?
            """
            cursor = db.execute_query(query, (threshold,))
            inventory_items = []
            
            for row in cursor.fetchall():
                product = Product.get_by_id(row[1])
                if product:
                    inventory_items.append(cls(
                        inventory_id=row[0],
                        product=product,
                        quantity_in_stock=row[2],
                        last_stock_update=row[3]
                    ))
            return inventory_items
        except Exception as e:
            print(f"Error listing low stock products: {str(e)}")
            return []
        finally:
            db.close_connection()

    @classmethod
    def list_out_of_stock_products(cls) -> List['Inventory']:
        """List products that are out of stock."""
        return cls.list_low_stock_products(1)

    @classmethod
    def list_all_products(cls) -> List['Inventory']:
        """List all products in the inventory, along with their quantities."""
        db = DatabaseConnector()
        try:
            query = """
            SELECT i.InventoryID, i.ProductID, i.QuantityInStock, i.LastStockUpdate
            FROM Inventory i
            ORDER BY i.QuantityInStock DESC
            """
            cursor = db.execute_query(query)
            inventory_items = []
            
            for row in cursor.fetchall():
                product = Product.get_by_id(row[1])
                if product:
                    inventory_items.append(cls(
                        inventory_id=row[0],
                        product=product,
                        quantity_in_stock=row[2],
                        last_stock_update=row[3]
                    ))
            return inventory_items
        except Exception as e:
            print(f"Error listing all products: {str(e)}")
            return []
        finally:
            db.close_connection() 