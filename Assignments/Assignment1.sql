use TechShop;
--create table "Customers" ( "CustomerID" Varchar primary key, "FirstName" Varchar(20), "LastName" Varchar(20), "Email" Varchar(40), "Phone" Varchar(10), "Address" Varchar(50));
--create table "Products" ("ProductID" varchar(20) primary key, "ProductName" Varchar(30), "Description" Varchar(80), Price float(8));
--create table "Orders" ("OrderID" Varchar(20) primary key, "CustomerID" varchar, foreign key("CustomerID") references Customers("CustomerID"));
--alter table "Orders" add "OrderDate" Date, TotalAmount decimal(8,2);

--exec sp_help 'Customers';

-- size of varchar is 1 for CustomreID which is primary key and reference foreign key for Orders table.
--alter table Orders drop constraint FK__Orders__Customer__3B75D760;
--alter table Customers drop constraint PK__Customer__A4AE64B8131CAED3;

--alter table Customers alter column CustomerID varchar(20) not null;
--alter table Orders alter column CustomerID varchar(20);

--alter table Customers add constraint pk_customer primary key(CustomerID);
--alter table Orders add constraint fk_orders foreign key(CustomerID) references Customers(CustomerID);

--create table OrderDetails ( OrderDetailID varchar(30) not null primary key , OrderID varchar(20), ProductID varchar(20), Quantity int, foreign key(OrderID) references Orders(OrderID), foreign key (ProductID) references Products(ProductID));
--create table Inventory(InventoryID varchar(20) not null primary key, ProductID varchar(20), foreign key(ProductID) references Products(ProductID), QuantityInStock int, LastStockUpdate int);

--alter database sis modify name = "TechShop";

