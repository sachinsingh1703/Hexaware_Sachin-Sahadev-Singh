import configparser
from typing import Dict

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file: str) -> Dict[str, str]:
        """
        Read database connection properties from a property file and return connection string.
        
        Args:
            property_file (str): Path to the property file
            
        Returns:
            Dict[str, str]: Dictionary containing connection parameters
        """
        try:
            config = configparser.ConfigParser()
            config.read(property_file)
            
            db_config = {
                'driver': config.get('Database', 'driver'),
                'server': config.get('Database', 'server'),
                'database': config.get('Database', 'database'),
                'trusted_connection': config.get('Database', 'trusted_connection')
            }
            
            return db_config
            
        except Exception as e:
            print(f"Error reading property file: {str(e)}")
            return {} 