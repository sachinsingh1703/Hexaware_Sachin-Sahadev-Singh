import pyodbc
from typing import Optional
from .db_property_util import DBPropertyUtil
from exception.techshop_exceptions import DatabaseConnectionError

class DBConnUtil:
    _connection = None
    
    @classmethod
    def get_connection(cls, property_file: str = "database.properties") -> Optional[pyodbc.Connection]:
        """
        Get a database connection using properties from the specified property file.
        
        Args:
            property_file (str): Path to the property file (default: "database.properties")
            
        Returns:
            Optional[pyodbc.Connection]: Database connection object or None if connection fails
            
        Raises:
            DatabaseConnectionError: If connection cannot be established
        """
        try:
            if not cls._connection or cls._connection.closed:
                # Get connection parameters from property file
                db_config = DBPropertyUtil.get_connection_string(property_file)
                
                if not db_config:
                    raise DatabaseConnectionError("Failed to read database configuration")
                
                # Build connection string
                connection_string = (
                    f"DRIVER={db_config['driver']};"
                    f"SERVER={db_config['server']};"
                    f"DATABASE={db_config['database']};"
                    f"Trusted_Connection={db_config['trusted_connection']};"
                )
                
                # Create connection
                cls._connection = pyodbc.connect(connection_string)
                
            return cls._connection
            
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}")
    
    @classmethod
    def close_connection(cls) -> None:
        """Close the database connection if it exists."""
        if cls._connection and not cls._connection.closed:
            try:
                cls._connection.close()
            except Exception as e:
                print(f"Error closing database connection: {str(e)}")
            finally:
                cls._connection = None 