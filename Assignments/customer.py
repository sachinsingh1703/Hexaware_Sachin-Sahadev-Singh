from database_connector import DatabaseConnector
from exceptions import InvalidDataException
import re

class Customer:
    def __init__(self, first_name: str, last_name: str, email: str, phone: str = None, address: str = None, customer_id: int = None):
        self._customer_id = customer_id
        self._first_name = None
        self._last_name = None
        self._email = None
        self._phone = None
        self._address = None
        
        # Set values using properties to ensure validation
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        
        self._db = DatabaseConnector()

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value or not value.strip():
            raise InvalidDataException("First name cannot be empty")
        self._first_name = value.strip()

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value or not value.strip():
            raise InvalidDataException("Last name cannot be empty")
        self._last_name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not value or not value.strip():
            raise InvalidDataException("Email cannot be empty")
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise InvalidDataException("Invalid email format")
        self._email = value.strip().lower()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if value:
            # Basic phone number validation (allows various formats)
            phone_pattern = r'^\+?1?\d{9,15}$'
            if not re.match(phone_pattern, value.strip()):
                raise InvalidDataException("Invalid phone number format")
            self._phone = value.strip()
        else:
            self._phone = None

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = value.strip() if value else None

    def save(self) -> bool:
        """Save or update customer information in the database."""
        try:
            if self._customer_id:
                # Update existing customer
                query = """
                UPDATE Customers 
                SET FirstName = ?, LastName = ?, Email = ?, Phone = ?, Address = ?
                WHERE CustomerID = ?
                """
                params = (self.first_name, self.last_name, self.email, 
                         self.phone, self.address, self._customer_id)
                cursor = self._db.execute_query(query, params)
                if cursor:
                    self._db.commit()
                    return True
            else:
                # Insert new customer
                insert_query = """
                INSERT INTO Customers (FirstName, LastName, Email, Phone, Address)
                VALUES (?, ?, ?, ?, ?)
                """
                params = (self.first_name, self.last_name, self.email, 
                         self.phone, self.address)
                
                cursor = self._db.execute_query(insert_query, params)
                if cursor:
                    self._db.commit()
                    
                    # Get the inserted ID
                    id_query = "SELECT IDENT_CURRENT('Customers')"
                    cursor = self._db.execute_query(id_query)
                    if cursor:
                        row = cursor.fetchone()
                        if row:
                            self._customer_id = int(row[0])
                            return True
            return False
        except Exception as e:
            print(f"Error saving customer: {str(e)}")
            return False

    def calculate_total_orders(self) -> int:
        """Calculate the total number of orders placed by this customer."""
        try:
            query = """
            SELECT COUNT(*) 
            FROM Orders 
            WHERE CustomerID = ?
            """
            cursor = self._db.execute_query(query, (self._customer_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error calculating total orders: {str(e)}")
            return 0

    def get_customer_details(self) -> dict:
        """Retrieve detailed information about the customer."""
        details = {
            'customer_id': self._customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'total_orders': self.calculate_total_orders()
        }
        return details

    def update_customer_info(self, **kwargs) -> bool:
        """Update customer information."""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            return self.save()
        except Exception as e:
            print(f"Error updating customer info: {str(e)}")
            return False

    @classmethod
    def get_by_id(cls, customer_id: int):
        """Retrieve a customer by their ID."""
        db = DatabaseConnector()
        try:
            query = """
            SELECT CustomerID, FirstName, LastName, Email, Phone, Address
            FROM Customers
            WHERE CustomerID = ?
            """
            cursor = db.execute_query(query, (customer_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    customer_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    phone=row[4],
                    address=row[5]
                )
            return None
        except Exception as e:
            print(f"Error retrieving customer: {str(e)}")
            return None
        finally:
            db.close_connection()

    @classmethod
    def get_by_email(cls, email: str):
        """Retrieve a customer by their email."""
        db = DatabaseConnector()
        try:
            query = """
            SELECT CustomerID, FirstName, LastName, Email, Phone, Address
            FROM Customers
            WHERE Email = ?
            """
            cursor = db.execute_query(query, (email,))
            row = cursor.fetchone()
            if row:
                return cls(
                    customer_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    phone=row[4],
                    address=row[5]
                )
            return None
        except Exception as e:
            print(f"Error retrieving customer: {str(e)}")
            return None
        finally:
            db.close_connection() 