use TechShopDB;

-- Insert data into Customers table
INSERT INTO Customers (FirstName, LastName, Email, Phone, Address)
VALUES 
('John', 'Doe', 'john.doe@email.com', '555-0101', '123 Main St'),
('Jane', 'Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave'),
('Mike', 'Johnson', 'mike.j@email.com', '555-0103', '789 Pine Rd');

-- Insert data into Products table
INSERT INTO Products (ProductName, Description, Price)
VALUES 
('Laptop Pro X', 'High-performance laptop with 16GB RAM', 1299.99),
('Wireless Mouse', 'Ergonomic wireless mouse with long battery life', 49.99),
('4K Monitor', '27-inch 4K Ultra HD Display', 399.99),
('Gaming Keyboard', 'Mechanical RGB Gaming Keyboard', 129.99);

-- Insert data into Orders table
INSERT INTO Orders (CustomerID, OrderDate, TotalAmount)
VALUES 
(3, '2024-03-15', 1349.98),
(8, '2024-03-16', 529.98),
(9, '2024-03-16', 399.99);

INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
VALUES 
(3, 8, 1),  -- Order 3 ordered 1 Laptop Pro X
(3, 9, 1),  -- and 1 Wireless Mouse
(4, 6, 1),  -- Order 4 ordered 1 4K Monitor
(4, 9, 1),  -- and 1 Wireless Mouse
(5, 7, 1);  -- Order 5 ordered 1 Gaming Keyboard

INSERT INTO Inventory (ProductID, QuantityInStock, LastStockUpdate)
VALUES 
(4, 50, GETDATE()),   -- Laptop Pro X
(5, 100, GETDATE()),  -- Wireless Mouse
(6, 30, GETDATE()),   -- 4K Monitor
(7, 75, GETDATE());   -- Gaming Keyboard

select * from Customers;
select * from Inventory;
select * from OrderDetails;
select * from Orders;
select * from Products;