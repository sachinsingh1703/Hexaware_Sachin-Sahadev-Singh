from database_connector import DatabaseConnector
import time

def verify_table_exists(cursor, table_name):
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = '{table_name}'
    """)
    return cursor.fetchone()[0] > 0

def create_database():
    # First create database if it doesn't exist
    db = DatabaseConnector()
    db.database = "master"  # Explicitly connect to master first
    connection = db.get_connection()
    
    if connection:
        try:
            # Set autocommit mode for database creation
            connection.autocommit = True
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute("SELECT database_id FROM sys.databases WHERE name = 'TechShopDB'")
            result = cursor.fetchone()
            
            if not result:
                # Create the database
                cursor.execute("CREATE DATABASE TechShopDB")
                print("Database created successfully!")
                # Wait a moment to ensure database is ready
                time.sleep(1)
            else:
                print("Database already exists.")
            
            # Close the initial connection
            cursor.close()
            db.close_connection()
            
            # Create a new connection to TechShopDB for creating tables
            db = DatabaseConnector()  # This will now connect to TechShopDB by default
            connection = db.get_connection()
            
            if connection:
                cursor = connection.cursor()
                
                # Verify we're in the correct database
                cursor.execute("SELECT DB_NAME()")
                current_db = cursor.fetchone()[0]
                print(f"Connected to database: {current_db}")
                
                # Create tables one by one with verification
                tables = {
                    'Customers': """
                    CREATE TABLE Customers (
                        CustomerID INT PRIMARY KEY IDENTITY(1,1),
                        FirstName NVARCHAR(50) NOT NULL,
                        LastName NVARCHAR(50) NOT NULL,
                        Email NVARCHAR(100) NOT NULL,
                        Phone NVARCHAR(20),
                        Address NVARCHAR(200)
                    )
                    """,
                    'Products': """
                    CREATE TABLE Products (
                        ProductID INT PRIMARY KEY IDENTITY(1,1),
                        ProductName NVARCHAR(100) NOT NULL,
                        Description NVARCHAR(500),
                        Price DECIMAL(10, 2) NOT NULL
                    )
                    """,
                    'Orders': """
                    CREATE TABLE Orders (
                        OrderID INT PRIMARY KEY IDENTITY(1,1),
                        CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
                        OrderDate DATETIME DEFAULT GETDATE(),
                        TotalAmount DECIMAL(10, 2)
                    )
                    """,
                    'OrderDetails': """
                    CREATE TABLE OrderDetails (
                        OrderDetailID INT PRIMARY KEY IDENTITY(1,1),
                        OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
                        ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
                        Quantity INT NOT NULL
                    )
                    """,
                    'Inventory': """
                    CREATE TABLE Inventory (
                        InventoryID INT PRIMARY KEY IDENTITY(1,1),
                        ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
                        QuantityInStock INT NOT NULL,
                        LastStockUpdate DATETIME DEFAULT GETDATE()
                    )
                    """
                }
                
                for table_name, create_query in tables.items():
                    try:
                        if not verify_table_exists(cursor, table_name):
                            cursor.execute(create_query)
                            connection.commit()
                            print(f"Table {table_name} created successfully!")
                        else:
                            print(f"Table {table_name} already exists.")
                            # Verify table structure
                            cursor.execute(f"SELECT TOP 0 * FROM {table_name}")
                            print(f"Table {table_name} is accessible and has valid structure.")
                    except Exception as table_error:
                        print(f"Error creating/verifying table {table_name}: {str(table_error)}")
                
                # Final verification of all tables
                print("\nFinal verification of tables:")
                for table_name in tables.keys():
                    try:
                        cursor.execute(f"SELECT TOP 0 * FROM {table_name}")
                        print(f"✓ Table {table_name} is valid and accessible")
                    except Exception as e:
                        print(f"✗ Error accessing table {table_name}: {str(e)}")
                    
                cursor.close()
                
        except Exception as e:
            print(f"Error creating database schema: {str(e)}")
        finally:
            if connection:
                db.close_connection()
    else:
        print("Could not establish database connection")

if __name__ == "__main__":
    create_database()
    
    # Verify the connection and tables after setup
    print("\nVerifying final database connection...")
    db = DatabaseConnector()
    db.verify_connection() 