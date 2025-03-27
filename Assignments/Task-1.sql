USE techshop;

CREATE TABLE Customers (
CustomerID INT IDENTITY(1000,1) PRIMARY KEY,
FirstName NVARCHAR(50) NOT NULL,
LastName NVARCHAR(50) NOT NULL,
Email NVARCHAR(100) UNIQUE NOT NULL,
Phone NVARCHAR(15) UNIQUE NOT NULL,
Address NVARCHAR(255) NULL
);

CREATE TABLE Products (
ProductID INT IDENTITY(2000,1) PRIMARY KEY,
ProductName NVARCHAR(100) NOT NULL,
Description NVARCHAR(255) NULL,
Price DECIMAL(10,2) NOT NULL
);


CREATE TABLE Orders (
OrderID INT IDENTITY(3000,1) PRIMARY KEY,
CustomerID INT NOT NULL,
OrderDate DATETIME DEFAULT GETDATE(),
TotalAmount DECIMAL(10,2) NOT NULL,
CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE
);


CREATE TABLE OrderDetails (
OrderDetailID INT IDENTITY(4000,1) PRIMARY KEY,
OrderID INT NOT NULL,
ProductID INT NOT NULL,
Quantity INT NOT NULL CHECK (Quantity > 0),
CONSTRAINT FK_OrderDetails_Orders FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
CONSTRAINT FK_OrderDetails_Products FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
);


CREATE TABLE Inventory (
InventoryID INT IDENTITY(5000,1) PRIMARY KEY,
ProductID INT NOT NULL UNIQUE,
QuantityInStock INT NOT NULL CHECK (QuantityInStock >= 0),
LastStockUpdate DATETIME DEFAULT GETDATE(),
CONSTRAINT FK_Inventory_Products FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
);

INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) VALUES
('John', 'Cena', 'john.cena@wwe.com', '9998887771', '123 WWE Street, USA'),
('Dwayne', 'Johnson', 'dwayne.johnson@wwe.com', '9998887772', '456 Hollywood Blvd, USA'),
('Steve', 'Austin', 'steve.austin@wwe.com', '9998887773', '316 Broken Skull Ranch, USA'),
('Paul', 'Levesque', 'tripleh@wwe.com', '9998887774', '789 King of Kings Ave, USA'),
('Randy', 'Orton', 'randy.orton@wwe.com', '9998887775', '321 Apex Predator Lane, USA'),
('Roman', 'Reigns', 'roman.reigns@wwe.com', '9998887776', '111 Tribal Chief Road, USA'),
('Brock', 'Lesnar', 'brock.lesnar@wwe.com', '9998887777', '222 Beast Incarnate Drive, USA'),
('Undertaker', 'Deadman', 'undertaker@wwe.com', '9998887778', '666 Dark Alley, USA'),
('Shawn', 'Michaels', 'shawn.michaels@wwe.com', '9998887779', '555 Sweet Chin Music Street, USA'),
('Edge', 'RatedR', 'edge@wwe.com', '9998887780', '777 Spear Avenue, USA');


INSERT INTO Products (ProductName, Description, Price) VALUES
('WWE Championship Belt', 'Replica of the official WWE Championship', 299.99),
('John Cena T-Shirt', 'Never Give Up - Hustle, Loyalty, Respect', 24.99),
('The Rock Action Figure', 'Dwayne The Rock Johnson collectible figure', 19.99),
('Stone Cold Beer Mug', 'Austin 3:16 beer glass', 14.99),
('Triple H Sledgehammer', 'Replica of Triple H’s signature weapon', 49.99),
('Randy Orton RKO Hoodie', 'Apex Predator themed hoodie', 39.99),
('Roman Reigns Gloves', 'Tribal Chief Special Edition gloves', 29.99),
('Brock Lesnar Suplex City Shirt', 'Suplex City graphic tee', 22.99),
('Undertaker Hat & Coat Set', 'Deadman’s signature attire', 99.99),
('Edge Rated R Necklace', 'Rated R Superstar themed pendant', 15.99);


INSERT INTO Orders (CustomerID, OrderDate, TotalAmount) VALUES
(1000, '2025-03-01', 324.98),
(1001, '2025-03-02', 44.98),
(1002, '2025-03-03', 19.99),
(1003, '2025-03-04', 64.98),
(1004, '2025-03-05', 39.99),
(1005, '2025-03-06', 29.99),
(1006, '2025-03-07', 22.99),
(1007, '2025-03-08', 99.99),
(1008, '2025-03-09', 15.99),
(1009, '2025-03-10', 49.99);


INSERT INTO OrderDetails (OrderID, ProductID, Quantity) VALUES
(3000, 2000, 1), -- WWE Championship Belt
(3001, 2001, 1), -- John Cena T-Shirt
(3002, 2002, 1), -- The Rock Action Figure
(3003, 2003, 2), -- Stone Cold Beer Mug
(3004, 2004, 1), -- Triple H Sledgehammer
(3005, 2005, 1), -- Randy Orton RKO Hoodie
(3006, 2006, 1), -- Roman Reigns Gloves
(3007, 2007, 1), -- Brock Lesnar Suplex City Shirt
(3008, 2008, 1), -- Undertaker Hat & Coat Set
(3009, 2009, 1); -- Edge Rated R Necklace


INSERT INTO Inventory (ProductID, QuantityInStock, LastStockUpdate) VALUES
(2000, 10, '2025-02-28'),
(2001, 50, '2025-02-28'),
(2002, 30, '2025-02-28'),
(2003, 40, '2025-02-28'),
(2004, 15, '2025-02-28'),
(2005, 25, '2025-02-28'),
(2006, 20, '2025-02-28'),
(2007, 35, '2025-02-28'),
(2008, 5, '2025-02-28'),
(2009, 45, '2025-02-28');

