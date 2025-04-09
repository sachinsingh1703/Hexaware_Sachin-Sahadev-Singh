import configparser
import os

class PropertyUtil:
    @staticmethod
    def get_property_string() -> str:
        """Return connection string for the Hospital Management database"""
        return (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-OTOASK5;"
            "DATABASE=Hospital_Management;"
            "Trusted_Connection=yes;"
        ) 