# TechShop Management System

A comprehensive management system for TechShop, an electronic gadgets retailer. This system handles customer information, product management, order processing, and inventory tracking.

## Features

- Customer Management
  - Store and manage customer information
  - Track customer orders
  - Update customer details
  
- Product Management
  - Maintain product catalog
  - Track product details and pricing
  - Check product availability
  
- Order Processing
  - Create and manage orders
  - Track order status
  - Calculate order totals
  - Apply discounts
  
- Inventory Management
  - Track product stock levels
  - Monitor low stock items
  - Calculate inventory value
  - Update stock quantities

## Prerequisites

- Python 3.8 or higher
- SQL Server 2019 or higher
- SQL Server Native Client
- pyodbc

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd techshop
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Configure the database:
- Make sure SQL Server is running
- Update the server name in `database_connector.py` if needed
- Run the database setup script:
```bash
python database_setup.py
```

## Usage

### Customer Management

```python
from customer import Customer

# Create a new customer
customer = Customer(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    phone="1234567890",
    address="123 Main St"
)
customer.save()

# Get customer details
details = customer.get_customer_details()
print(details)

# Update customer information
customer.update_customer_info(
    phone="0987654321",
    address="456 Oak Ave"
)
```

### Product Management

```python
from product import Product
from decimal import Decimal

# Create a new product
product = Product(
    product_name="Smartphone X",
    description="Latest smartphone model",
    price=Decimal("999.99")
)
product.save()

# Get product details
details = product.get_product_details()
print(details)

# Check if product is in stock
in_stock = product.is_product_in_stock()
```

### Order Processing

```python
from order import Order, OrderDetail
from customer import Customer
from product import Product

# Create an order
customer = Customer.get_by_id(1)
order = Order(customer=customer)
order.save()

# Add products to the order
product = Product.get_by_id(1)
order.add_order_detail(
    product=product,
    quantity=2,
    discount=Decimal("10.00")
)

# Get order details
details = order.get_order_details()
print(details)

# Update order status
order.update_order_status("Shipped")
```

### Inventory Management

```python
from inventory import Inventory
from product import Product

# Create/update inventory
product = Product.get_by_id(1)
inventory = Inventory(product=product, quantity_in_stock=100)
inventory.save()

# Add stock
inventory.add_to_inventory(50)

# Remove stock
inventory.remove_from_inventory(20)

# Check availability
available = inventory.is_product_available(10)

# List low stock products
low_stock = Inventory.list_low_stock_products(threshold=10)
```

## Error Handling

The system includes comprehensive error handling for various scenarios:

- Data validation errors
- Insufficient stock errors
- Database connection errors
- Concurrent access issues
- Payment processing errors

All exceptions are logged and provide meaningful error messages to help diagnose and resolve issues.

## Database Schema

The system uses the following database tables:

- Customers
- Products
- Orders
- OrderDetails
- Inventory
- Payments

Each table includes appropriate foreign key relationships and constraints to maintain data integrity.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 