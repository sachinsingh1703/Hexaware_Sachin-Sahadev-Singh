from database_connector import DatabaseConnector
from exceptions import InvalidDataException
from decimal import Decimal
from typing import List, Optional

class Product:
    def __init__(self, product_name: str, description: str, price: Decimal, product_id: int = None):
        self._product_id = product_id
        self._product_name = None
        self._description = None
        self._price = None
        
        # Set values using properties to ensure validation
        self.product_name = product_name
        self.description = description
        self.price = price
        
        self._db = DatabaseConnector()

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def product_name(self) -> str:
        return self._product_name

    @product_name.setter
    def product_name(self, value: str):
        if not value or not value.strip():
            raise InvalidDataException("Product name cannot be empty")
        self._product_name = value.strip()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value.strip() if value else None

    @property
    def price(self) -> Decimal:
        return self._price

    @price.setter
    def price(self, value: Decimal):
        if not isinstance(value, (int, float, Decimal)):
            raise InvalidDataException("Price must be a numeric value")
        value = Decimal(str(value))
        if value < 0:
            raise InvalidDataException("Price cannot be negative")
        self._price = value

    def save(self) -> bool:
        """Save or update product information in the database."""
        try:
            if self._product_id:
                # Update existing product
                query = """
                UPDATE Products 
                SET ProductName = ?, Description = ?, Price = ?
                WHERE ProductID = ?
                """
                params = (self.product_name, self.description, 
                         float(self.price), self._product_id)
                cursor = self._db.execute_query(query, params)
                if cursor:
                    self._db.commit()
                    return True
            else:
                # Insert new product
                insert_query = """
                INSERT INTO Products (ProductName, Description, Price)
                VALUES (?, ?, ?)
                """
                params = (self.product_name, self.description, float(self.price))
                
                cursor = self._db.execute_query(insert_query, params)
                if cursor:
                    self._db.commit()
                    
                    # Get the inserted ID
                    id_query = "SELECT IDENT_CURRENT('Products')"
                    cursor = self._db.execute_query(id_query)
                    if cursor:
                        row = cursor.fetchone()
                        if row:
                            self._product_id = int(row[0])
                            return True
            return False
        except Exception as e:
            print(f"Error saving product: {str(e)}")
            return False

    def get_product_details(self) -> dict:
        """Retrieve detailed information about the product."""
        details = {
            'product_id': self._product_id,
            'product_name': self.product_name,
            'description': self.description,
            'price': float(self.price),
            'in_stock': self.is_product_in_stock()
        }
        return details

    def update_product_info(self, **kwargs) -> bool:
        """Update product information."""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            return self.save()
        except Exception as e:
            print(f"Error updating product info: {str(e)}")
            return False

    def is_product_in_stock(self) -> bool:
        """Check if the product is currently in stock."""
        try:
            query = """
            SELECT QuantityInStock 
            FROM Inventory 
            WHERE ProductID = ?
            """
            cursor = self._db.execute_query(query, (self._product_id,))
            row = cursor.fetchone()
            return row and row[0] > 0
        except Exception as e:
            print(f"Error checking stock: {str(e)}")
            return False

    @classmethod
    def get_by_id(cls, product_id: int) -> Optional['Product']:
        """Retrieve a product by its ID."""
        db = DatabaseConnector()
        try:
            query = """
            SELECT ProductID, ProductName, Description, Price
            FROM Products
            WHERE ProductID = ?
            """
            cursor = db.execute_query(query, (product_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    product_id=row[0],
                    product_name=row[1],
                    description=row[2],
                    price=Decimal(str(row[3]))
                )
            return None
        except Exception as e:
            print(f"Error retrieving product: {str(e)}")
            return None
        finally:
            db.close_connection()

    @classmethod
    def search_products(cls, search_term: str = None, category: str = None) -> List['Product']:
        """Search for products based on name or category."""
        db = DatabaseConnector()
        try:
            query = "SELECT ProductID, ProductName, Description, Price FROM Products WHERE 1=1"
            params = []
            
            if search_term:
                query += " AND (ProductName LIKE ? OR Description LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern])
            
            cursor = db.execute_query(query, params)
            products = []
            for row in cursor.fetchall():
                products.append(cls(
                    product_id=row[0],
                    product_name=row[1],
                    description=row[2],
                    price=Decimal(str(row[3]))
                ))
            return products
        except Exception as e:
            print(f"Error searching products: {str(e)}")
            return []
        finally:
            db.close_connection() 