import pyodbc
from typing import Optional

class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.server = "DESKTOP-OTOASK5"
        self.database = "TechShopDB"  # Changed default database to TechShopDB
        self.trusted_connection = "yes"
        self.driver = "{SQL Server}"

    def get_connection(self) -> Optional[pyodbc.Connection]:
        """Get a database connection."""
        if not self.connection:
            try:
                connection_string = (
                    f"DRIVER={self.driver};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"Trusted_Connection={self.trusted_connection};"
                )
                self.connection = pyodbc.connect(connection_string)
                print(f"Successfully connected to database: {self.database}")  # Added connection confirmation
                return self.connection
            except pyodbc.Error as e:
                print(f"Error connecting to database: {str(e)}")
                return None
        return self.connection

    def verify_connection(self):
        """Verify database connection and table existence."""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                # Verify we're in the correct database
                cursor.execute("SELECT DB_NAME()")
                current_db = cursor.fetchone()[0]
                print(f"Currently connected to database: {current_db}")
                
                # Check if Customers table exists
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'Customers'
                """)
                table_exists = cursor.fetchone()[0] > 0
                print(f"Customers table exists: {table_exists}")
                
                cursor.close()
                return True
            except pyodbc.Error as e:
                print(f"Error verifying connection: {str(e)}")
                return False
        return False

    def use_database(self, database_name: str):
        """Change the current database."""
        self.database = database_name
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            finally:
                self.connection = None

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except pyodbc.Error as e:
                print(f"Error closing database connection: {str(e)}")

    def execute_query(self, query: str, params=None):
        """Execute a query and return results."""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor
            except pyodbc.Error as e:
                print(f"Error executing query: {str(e)}")
                return None
        return None

    def commit(self):
        """Commit the current transaction."""
        if self.connection:
            try:
                self.connection.commit()
            except pyodbc.Error as e:
                print(f"Error committing transaction: {str(e)}") 