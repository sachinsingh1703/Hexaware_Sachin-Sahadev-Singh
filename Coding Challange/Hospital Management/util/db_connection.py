import pyodbc
from util.property_util import PropertyUtil

class DBConnection:
    __connection = None

    @staticmethod
    def get_connection():
        """Get a database connection, creating it if it doesn't exist"""
        if DBConnection.__connection is None:
            try:
                conn_str = PropertyUtil.get_property_string()
                DBConnection.__connection = pyodbc.connect(conn_str)
            except Exception as e:
                raise Exception(f"Failed to connect to database: {str(e)}")
        
        return DBConnection.__connection 