class TechShopException(Exception):
    """Base exception class for TechShop application"""
    pass

class DatabaseConnectionError(TechShopException):
    """Raised when there is an error connecting to the database"""
    pass

class CustomerNotFoundError(TechShopException):
    """Raised when a customer is not found in the database"""
    pass

class ProductNotFoundError(TechShopException):
    """Raised when a product is not found in the database"""
    pass

class OrderNotFoundError(TechShopException):
    """Raised when an order is not found in the database"""
    pass

class InsufficientStockError(TechShopException):
    """Raised when there is insufficient stock for a product"""
    pass

class InvalidDataError(TechShopException):
    """Raised when invalid data is provided"""
    pass

class OrderProcessingError(TechShopException):
    """Raised when there is an error processing an order"""
    pass 