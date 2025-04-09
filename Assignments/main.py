from customer import Customer
from product import Product
from order import Order, OrderDetail
from inventory import Inventory
from decimal import Decimal
from datetime import datetime
import sys

class TechShopSystem:
    def __init__(self):
        self.current_customer = None

    def display_menu(self):
        print("\n=== TechShop Management System ===")
        print("1. Customer Registration")
        print("2. Product Catalog Management")
        print("3. Place Customer Order")
        print("4. Track Order Status")
        print("5. Inventory Management")
        print("6. Sales Reporting")
        print("7. Update Customer Account")
        print("8. Payment Processing")
        print("9. Product Search")
        print("0. Exit")
        return input("Enter your choice (0-9): ")

    def register_customer(self):
        """Customer Registration"""
        print("\n=== Customer Registration ===")
        try:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")

            # Check if email already exists
            existing_customer = Customer.get_by_email(email)
            if existing_customer:
                print("Error: Email already registered!")
                return

            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address
            )
            if customer.save():
                print("Customer registered successfully!")
                self.current_customer = customer
            else:
                print("Error registering customer.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def manage_product_catalog(self):
        """Product Catalog Management"""
        print("\n=== Product Catalog Management ===")
        print("1. Add New Product")
        print("2. Update Product")
        print("3. View Product Details")
        choice = input("Enter choice (1-3): ")

        try:
            if choice == "1":
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                price = Decimal(input("Enter product price: "))

                product = Product(
                    product_name=name,
                    description=description,
                    price=price
                )
                if product.save():
                    print("Product added successfully!")
                    # Initialize inventory for the new product
                    inventory = Inventory(product=product, quantity_in_stock=0)
                    inventory.save()
                else:
                    print("Error adding product.")

            elif choice == "2":
                product_id = int(input("Enter product ID to update: "))
                product = Product.get_by_id(product_id)
                if product:
                    name = input("Enter new name (or press enter to skip): ")
                    description = input("Enter new description (or press enter to skip): ")
                    price_str = input("Enter new price (or press enter to skip): ")

                    updates = {}
                    if name:
                        updates['product_name'] = name
                    if description:
                        updates['description'] = description
                    if price_str:
                        updates['price'] = Decimal(price_str)

                    if product.update_product_info(**updates):
                        print("Product updated successfully!")
                    else:
                        print("Error updating product.")
                else:
                    print("Product not found.")

            elif choice == "3":
                product_id = int(input("Enter product ID to view: "))
                product = Product.get_by_id(product_id)
                if product:
                    details = product.get_product_details()
                    print("\nProduct Details:")
                    for key, value in details.items():
                        print(f"{key}: {value}")
                else:
                    print("Product not found.")

        except Exception as e:
            print(f"Error: {str(e)}")

    def place_order(self):
        """Place Customer Order"""
        print("\n=== Place Order ===")
        try:
            if not self.current_customer:
                customer_id = int(input("Enter customer ID: "))
                self.current_customer = Customer.get_by_id(customer_id)
                if not self.current_customer:
                    print("Customer not found.")
                    return

            # Create new order
            order = Order(customer=self.current_customer)
            if not order.save():
                print("Error creating order.")
                return

            while True:
                product_id = input("Enter product ID (or press enter to finish): ")
                if not product_id:
                    break

                product = Product.get_by_id(int(product_id))
                if not product:
                    print("Product not found.")
                    continue

                quantity = int(input("Enter quantity: "))
                discount = Decimal(input("Enter discount percentage (0-100): "))

                try:
                    order.add_order_detail(
                        product=product,
                        quantity=quantity,
                        discount=discount
                    )
                    print("Product added to order.")
                except Exception as e:
                    print(f"Error adding product: {str(e)}")

            print("\nOrder Summary:")
            details = order.get_order_details()
            print(f"Order ID: {details['order_id']}")
            print(f"Total Amount: ${details['total_amount']:.2f}")
            print("Status: Processing")

        except Exception as e:
            print(f"Error: {str(e)}")

    def track_order(self):
        """Track Order Status"""
        print("\n=== Track Order Status ===")
        try:
            order_id = int(input("Enter order ID: "))
            order = Order.get_by_id(order_id)
            
            if order:
                details = order.get_order_details()
                print("\nOrder Details:")
                print(f"Order ID: {details['order_id']}")
                print(f"Customer: {details['customer']['first_name']} {details['customer']['last_name']}")
                print(f"Order Date: {details['order_date']}")
                print(f"Status: {details['status']}")
                print(f"Total Amount: ${details['total_amount']:.2f}")
                
                print("\nOrder Items:")
                for item in details['order_details']:
                    print(f"- {item['product']['product_name']}")
                    print(f"  Quantity: {item['quantity']}")
                    print(f"  Unit Price: ${item['unit_price']:.2f}")
                    print(f"  Discount: {item['discount']}%")
                    print(f"  Subtotal: ${item['subtotal']:.2f}")
            else:
                print("Order not found.")

        except Exception as e:
            print(f"Error: {str(e)}")

    def manage_inventory(self):
        """Inventory Management"""
        print("\n=== Inventory Management ===")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Stock Levels")
        print("4. List Low Stock Products")
        choice = input("Enter choice (1-4): ")

        try:
            if choice in ["1", "2"]:
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))
                
                inventory = Inventory.get_by_product_id(product_id)
                if not inventory:
                    print("Product not found in inventory.")
                    return

                if choice == "1":
                    if inventory.add_to_inventory(quantity):
                        print("Stock added successfully!")
                    else:
                        print("Error adding stock.")
                else:
                    if inventory.remove_from_inventory(quantity):
                        print("Stock removed successfully!")
                    else:
                        print("Error removing stock.")

            elif choice == "3":
                products = Inventory.list_all_products()
                print("\nCurrent Stock Levels:")
                for inv in products:
                    print(f"Product: {inv.product.product_name}")
                    print(f"Quantity in Stock: {inv.quantity_in_stock}")
                    print(f"Last Updated: {inv.last_stock_update}")
                    print()

            elif choice == "4":
                threshold = int(input("Enter stock threshold: "))
                low_stock = Inventory.list_low_stock_products(threshold)
                print("\nLow Stock Products:")
                for inv in low_stock:
                    print(f"Product: {inv.product.product_name}")
                    print(f"Quantity in Stock: {inv.quantity_in_stock}")
                    print(f"Last Updated: {inv.last_stock_update}")
                    print()

        except Exception as e:
            print(f"Error: {str(e)}")

    def generate_sales_report(self):
        """Sales Reporting"""
        print("\n=== Sales Report ===")
        # This would typically involve more complex queries and reporting
        # For demonstration, we'll show a simple report
        try:
            # Get all orders
            query = """
            SELECT 
                o.OrderID,
                c.FirstName + ' ' + c.LastName as CustomerName,
                o.OrderDate,
                o.TotalAmount,
                o.OrderStatus
            FROM Orders o
            JOIN Customers c ON o.CustomerID = c.CustomerID
            ORDER BY o.OrderDate DESC
            """
            db = Order._db
            cursor = db.execute_query(query)
            
            print("\nRecent Orders:")
            print("OrderID | Customer | Date | Amount | Status")
            print("-" * 60)
            
            total_sales = Decimal('0.00')
            for row in cursor.fetchall():
                print(f"{row[0]} | {row[1]} | {row[2]} | ${row[3]:.2f} | {row[4]}")
                total_sales += Decimal(str(row[3]))
            
            print("-" * 60)
            print(f"Total Sales: ${total_sales:.2f}")

        except Exception as e:
            print(f"Error: {str(e)}")

    def update_customer_account(self):
        """Update Customer Account"""
        print("\n=== Update Customer Account ===")
        try:
            if not self.current_customer:
                customer_id = int(input("Enter customer ID: "))
                self.current_customer = Customer.get_by_id(customer_id)
                if not self.current_customer:
                    print("Customer not found.")
                    return

            print("\nCurrent Information:")
            details = self.current_customer.get_customer_details()
            for key, value in details.items():
                if key != 'total_orders':
                    print(f"{key}: {value}")

            print("\nEnter new information (press enter to keep current value):")
            email = input("New email: ")
            phone = input("New phone: ")
            address = input("New address: ")

            updates = {}
            if email:
                updates['email'] = email
            if phone:
                updates['phone'] = phone
            if address:
                updates['address'] = address

            if self.current_customer.update_customer_info(**updates):
                print("Customer information updated successfully!")
            else:
                print("Error updating customer information.")

        except Exception as e:
            print(f"Error: {str(e)}")

    def process_payment(self):
        """Payment Processing"""
        print("\n=== Process Payment ===")
        try:
            order_id = int(input("Enter order ID: "))
            order = Order.get_by_id(order_id)
            
            if not order:
                print("Order not found.")
                return

            details = order.get_order_details()
            print(f"\nOrder Total: ${details['total_amount']:.2f}")
            
            payment_method = input("Enter payment method (Credit Card/Cash/Bank Transfer): ")
            
            # In a real system, you would integrate with a payment gateway here
            # For demonstration, we'll just record the payment
            query = """
            INSERT INTO Payments (OrderID, Amount, PaymentMethod, PaymentStatus)
            VALUES (?, ?, ?, 'Completed');
            """
            db = order._db
            cursor = db.execute_query(query, (order_id, details['total_amount'], payment_method))
            db.commit()
            
            # Update order status
            order.update_order_status("Shipped")
            print("Payment processed successfully!")

        except Exception as e:
            print(f"Error: {str(e)}")

    def search_products(self):
        """Product Search and Recommendations"""
        print("\n=== Product Search ===")
        try:
            search_term = input("Enter search term: ")
            products = Product.search_products(search_term)
            
            if products:
                print("\nSearch Results:")
                for product in products:
                    details = product.get_product_details()
                    print(f"\nProduct: {details['product_name']}")
                    print(f"Description: {details['description']}")
                    print(f"Price: ${details['price']:.2f}")
                    print(f"In Stock: {'Yes' if details['in_stock'] else 'No'}")
            else:
                print("No products found.")

        except Exception as e:
            print(f"Error: {str(e)}")

    def run(self):
        while True:
            choice = self.display_menu()
            
            if choice == "0":
                print("Thank you for using TechShop Management System!")
                sys.exit(0)
            elif choice == "1":
                self.register_customer()
            elif choice == "2":
                self.manage_product_catalog()
            elif choice == "3":
                self.place_order()
            elif choice == "4":
                self.track_order()
            elif choice == "5":
                self.manage_inventory()
            elif choice == "6":
                self.generate_sales_report()
            elif choice == "7":
                self.update_customer_account()
            elif choice == "8":
                self.process_payment()
            elif choice == "9":
                self.search_products()
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = TechShopSystem()
    system.run() 