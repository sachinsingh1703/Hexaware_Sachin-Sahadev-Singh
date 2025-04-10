from dao.techshop_dao import TechShopDAOImpl
from entity.model.entities import Customer, Product, Order, OrderDetail, Inventory
from exception.techshop_exceptions import *
from decimal import Decimal
from datetime import datetime
import sys

class MainModule:
    def __init__(self):
        self.dao = TechShopDAOImpl()

    def display_menu(self):
        print("\n=== TechShop Management System ===")
        print("1. Customer Management")
        print("2. Product Management")
        print("3. Order Management")
        print("4. Inventory Management")
        print("5. View All Data")
        print("0. Exit")
        return input("Enter your choice (0-5): ")

    def customer_menu(self):
        while True:
            print("\n=== Customer Management ===")
            print("1. Add New Customer")
            print("2. View Customer Details")
            print("3. Update Customer")
            print("0. Back to Main Menu")
            choice = input("Enter your choice (0-3): ")

            try:
                if choice == "1":
                    self.add_customer()
                elif choice == "2":
                    self.view_customer()
                elif choice == "3":
                    self.update_customer()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice!")
            except TechShopException as e:
                print(f"Error: {str(e)}")

    def product_menu(self):
        while True:
            print("\n=== Product Management ===")
            print("1. Add New Product")
            print("2. View Product Details")
            print("3. Update Product")
            print("0. Back to Main Menu")
            choice = input("Enter your choice (0-3): ")

            try:
                if choice == "1":
                    self.add_product()
                elif choice == "2":
                    self.view_product()
                elif choice == "3":
                    self.update_product()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice!")
            except TechShopException as e:
                print(f"Error: {str(e)}")

    def order_menu(self):
        while True:
            print("\n=== Order Management ===")
            print("1. Create New Order")
            print("2. View Order Details")
            print("0. Back to Main Menu")
            choice = input("Enter your choice (0-2): ")

            try:
                if choice == "1":
                    self.create_order()
                elif choice == "2":
                    self.view_order()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice!")
            except TechShopException as e:
                print(f"Error: {str(e)}")

    def inventory_menu(self):
        while True:
            print("\n=== Inventory Management ===")
            print("1. Update Product Stock")
            print("2. View Product Stock")
            print("0. Back to Main Menu")
            choice = input("Enter your choice (0-2): ")

            try:
                if choice == "1":
                    self.update_stock()
                elif choice == "2":
                    self.view_stock()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice!")
            except TechShopException as e:
                print(f"Error: {str(e)}")

    def view_data_menu(self):
        while True:
            print("\n=== View All Data ===")
            print("1. View All Customers")
            print("2. View All Products")
            print("3. View All Orders")
            print("4. View All Order Details")
            print("5. View All Inventory")
            print("0. Back to Main Menu")
            choice = input("Enter your choice (0-5): ")

            try:
                if choice == "1":
                    self.view_all_customers()
                elif choice == "2":
                    self.view_all_products()
                elif choice == "3":
                    self.view_all_orders()
                elif choice == "4":
                    self.view_all_order_details()
                elif choice == "5":
                    self.view_all_inventory()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice!")
                
                if choice in ["1", "2", "3", "4", "5"]:
                    input("\nPress Enter to continue...")
            except TechShopException as e:
                print(f"Error: {str(e)}")

    def add_customer(self):
        print("\n=== Add New Customer ===")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        phone = input("Enter Phone: ")
        address = input("Enter Address: ")

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )

        if self.dao.add_customer(customer):
            print("Customer added successfully!")
        else:
            raise OrderProcessingError("Failed to add customer")

    def view_customer(self):
        print("\n=== View Customer Details ===")
        customer_id = int(input("Enter Customer ID: "))
        customer = self.dao.get_customer_by_id(customer_id)
        
        if customer:
            print(f"\nCustomer ID: {customer.customer_id}")
            print(f"Name: {customer.first_name} {customer.last_name}")
            print(f"Email: {customer.email}")
            print(f"Phone: {customer.phone}")
            print(f"Address: {customer.address}")
        else:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")

    def update_customer(self):
        print("\n=== Update Customer ===")
        customer_id = int(input("Enter Customer ID: "))
        customer = self.dao.get_customer_by_id(customer_id)
        
        if customer:
            print("\nEnter new details (press Enter to keep current value):")
            first_name = input(f"First Name [{customer.first_name}]: ") or customer.first_name
            last_name = input(f"Last Name [{customer.last_name}]: ") or customer.last_name
            email = input(f"Email [{customer.email}]: ") or customer.email
            phone = input(f"Phone [{customer.phone}]: ") or customer.phone
            address = input(f"Address [{customer.address}]: ") or customer.address

            updated_customer = Customer(
                customer_id=customer_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address
            )

            if self.dao.update_customer(updated_customer):
                print("Customer updated successfully!")
            else:
                raise OrderProcessingError("Failed to update customer")
        else:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")

    def add_product(self):
        print("\n=== Add New Product ===")
        name = input("Enter Product Name: ")
        description = input("Enter Description: ")
        price = Decimal(input("Enter Price: "))

        product = Product(
            product_name=name,
            description=description,
            price=price
        )

        if self.dao.add_product(product):
            print("Product added successfully!")
        else:
            raise OrderProcessingError("Failed to add product")

    def view_product(self):
        print("\n=== View Product Details ===")
        product_id = int(input("Enter Product ID: "))
        product = self.dao.get_product_by_id(product_id)
        
        if product:
            print(f"\nProduct ID: {product.product_id}")
            print(f"Name: {product.product_name}")
            print(f"Description: {product.description}")
            print(f"Price: ${product.price}")
            
            # Get inventory information
            inventory = self.dao.get_inventory_by_product(product_id)
            if inventory:
                print(f"Quantity in Stock: {inventory.quantity_in_stock}")
                print(f"Last Stock Update: {inventory.last_stock_update}")
        else:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")

    def update_product(self):
        print("\n=== Update Product ===")
        product_id = int(input("Enter Product ID: "))
        product = self.dao.get_product_by_id(product_id)
        
        if product:
            print("\nEnter new details (press Enter to keep current value):")
            name = input(f"Name [{product.product_name}]: ") or product.product_name
            description = input(f"Description [{product.description}]: ") or product.description
            price_str = input(f"Price [{product.price}]: ")
            price = Decimal(price_str) if price_str else product.price

            updated_product = Product(
                product_id=product_id,
                product_name=name,
                description=description,
                price=price
            )

            if self.dao.update_product(updated_product):
                print("Product updated successfully!")
            else:
                raise OrderProcessingError("Failed to update product")
        else:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")

    def create_order(self):
        print("\n=== Create New Order ===")
        customer_id = int(input("Enter Customer ID: "))
        customer = self.dao.get_customer_by_id(customer_id)
        
        if not customer:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")

        # Create order
        order = Order(
            customer_id=customer_id,
            order_date=datetime.now(),
            total_amount=Decimal('0.00')
        )

        if not self.dao.create_order(order):
            raise OrderProcessingError("Failed to create order")

        # Add order details
        total_amount = Decimal('0.00')
        while True:
            add_item = input("\nAdd item to order? (y/n): ").lower()
            if add_item != 'y':
                break

            product_id = int(input("Enter Product ID: "))
            product = self.dao.get_product_by_id(product_id)
            
            if not product:
                print(f"Product with ID {product_id} not found")
                continue

            quantity = int(input("Enter Quantity: "))
            inventory = self.dao.get_inventory_by_product(product_id)
            
            if not inventory or inventory.quantity_in_stock < quantity:
                print(f"Insufficient stock for product {product.product_name}")
                continue

            order_detail = OrderDetail(
                order_id=order.order_id,
                product_id=product_id,
                quantity=quantity
            )

            if self.dao.add_order_detail(order_detail):
                # Update inventory
                inventory.quantity_in_stock -= quantity
                self.dao.update_inventory(inventory)
                
                # Update total amount
                total_amount += product.price * Decimal(str(quantity))
            else:
                print("Failed to add item to order")

        # Update order total
        order.total_amount = total_amount
        if self.dao.create_order(order):
            print(f"\nOrder created successfully! Total Amount: ${total_amount}")
        else:
            raise OrderProcessingError("Failed to update order total")

    def view_order(self):
        print("\n=== View Order Details ===")
        order_id = int(input("Enter Order ID: "))
        order = self.dao.get_order_by_id(order_id)
        
        if order:
            print(f"\nOrder ID: {order.order_id}")
            print(f"Customer ID: {order.customer_id}")
            print(f"Order Date: {order.order_date}")
            print(f"Total Amount: ${order.total_amount}")
        else:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")

    def update_stock(self):
        print("\n=== Update Product Stock ===")
        product_id = int(input("Enter Product ID: "))
        product = self.dao.get_product_by_id(product_id)
        
        if not product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")

        inventory = self.dao.get_inventory_by_product(product_id)
        if inventory:
            print(f"Current Stock: {inventory.quantity_in_stock}")
            quantity = int(input("Enter New Stock Quantity: "))
            
            inventory.quantity_in_stock = quantity
            inventory.last_stock_update = datetime.now()
            
            if self.dao.update_inventory(inventory):
                print("Stock updated successfully!")
            else:
                raise OrderProcessingError("Failed to update stock")
        else:
            raise ProductNotFoundError(f"No inventory found for product ID {product_id}")

    def view_stock(self):
        print("\n=== View Product Stock ===")
        product_id = int(input("Enter Product ID: "))
        inventory = self.dao.get_inventory_by_product(product_id)
        
        if inventory:
            product = self.dao.get_product_by_id(product_id)
            print(f"\nProduct: {product.product_name}")
            print(f"Quantity in Stock: {inventory.quantity_in_stock}")
            print(f"Last Updated: {inventory.last_stock_update}")
        else:
            raise ProductNotFoundError(f"No inventory found for product ID {product_id}")

    def view_all_customers(self):
        customers = self.dao.get_all_customers()
        if not customers:
            print("\nNo customers found.")
            return

        print("\n=== All Customers ===")
        print("\nID  | First Name    | Last Name     | Email                  | Phone          | Address")
        print("-" * 85)
        for customer in customers:
            print(f"{customer.customer_id:<4} | {customer.first_name:<13} | {customer.last_name:<12} | {customer.email:<22} | {customer.phone:<14} | {customer.address}")

    def view_all_products(self):
        products = self.dao.get_all_products()
        if not products:
            print("\nNo products found.")
            return

        print("\n=== All Products ===")
        print("\nID  | Product Name      | Description                | Price")
        print("-" * 65)
        for product in products:
            print(f"{product.product_id:<4} | {product.product_name:<16} | {product.description:<24} | ${float(product.price):.2f}")

    def view_all_orders(self):
        orders = self.dao.get_all_orders()
        if not orders:
            print("\nNo orders found.")
            return

        print("\n=== All Orders ===")
        print("\nOrder ID | Customer ID | Order Date          | Total Amount")
        print("-" * 55)
        for order in orders:
            print(f"{order.order_id:<9} | {order.customer_id:<11} | {order.order_date} | ${float(order.total_amount):.2f}")

    def view_all_order_details(self):
        order_details = self.dao.get_all_order_details()
        if not order_details:
            print("\nNo order details found.")
            return

        print("\n=== All Order Details ===")
        print("\nDetail ID | Order ID | Product Name      | Quantity | Unit Price | Total")
        print("-" * 75)
        for detail in order_details:
            total = float(detail.unit_price * detail.quantity)
            print(f"{detail.order_detail_id:<10} | {detail.order_id:<8} | {detail.product_name:<16} | {detail.quantity:<8} | ${float(detail.unit_price):<9.2f} | ${total:.2f}")

    def view_all_inventory(self):
        inventory_items = self.dao.get_all_inventory()
        if not inventory_items:
            print("\nNo inventory items found.")
            return

        print("\n=== All Inventory ===")
        print("\nInventory ID | Product Name      | Quantity in Stock | Last Updated")
        print("-" * 70)
        for item in inventory_items:
            print(f"{item.inventory_id:<12} | {item.product_name:<16} | {item.quantity_in_stock:<16} | {item.last_stock_update}")

    def run(self):
        while True:
            choice = self.display_menu()
            
            try:
                if choice == "0":
                    print("Thank you for using TechShop Management System!")
                    sys.exit(0)
                elif choice == "1":
                    self.customer_menu()
                elif choice == "2":
                    self.product_menu()
                elif choice == "3":
                    self.order_menu()
                elif choice == "4":
                    self.inventory_menu()
                elif choice == "5":
                    self.view_data_menu()
                else:
                    print("Invalid choice!")
            except TechShopException as e:
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    app = MainModule()
    app.run() 