class InvalidDataException(Exception):
    """Exception raised for invalid data inputs."""
    pass

class InsufficientStockException(Exception):
    """Exception raised when product stock is insufficient."""
    pass

class IncompleteOrderException(Exception):
    """Exception raised when order details are incomplete."""
    pass

class PaymentFailedException(Exception):
    """Exception raised when payment processing fails."""
    pass

class AuthenticationException(Exception):
    """Exception raised for authentication failures."""
    pass

class AuthorizationException(Exception):
    """Exception raised for authorization failures."""
    pass

class ConcurrencyException(Exception):
    """Exception raised for concurrent data modification conflicts."""
    pass

class DatabaseException(Exception):
    """Exception raised for database-related errors."""
    pass 