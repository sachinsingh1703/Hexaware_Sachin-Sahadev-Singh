use TechShop;

----TASK 1----
/*
create table "Customers" ( "CustomerID" Varchar primary key, "FirstName" Varchar(20), "LastName" Varchar(20), "Email" Varchar(40), "Phone" Varchar(10), "Address" Varchar(50));
create table "Products" ("ProductID" varchar(20) primary key, "ProductName" Varchar(30), "Description" Varchar(80), Price float(8));
create table "Orders" ("OrderID" Varchar(20) primary key, "CustomerID" varchar, foreign key("CustomerID") references Customers("CustomerID"));
alter table "Orders" add "OrderDate" Date, TotalAmount decimal(8,2);
*/

---size of varchar is 1 for CustomreID which is primary key and reference foreign key for Orders table, so had to alter---
/*
alter table Orders drop constraint FK__Orders__Customer__3B75D760;
alter table Customers drop constraint PK__Customer__A4AE64B8131CAED3;

alter table Customers alter column CustomerID varchar(20) not null;
alter table Orders alter column CustomerID varchar(20);

alter table Customers add constraint pk_customer primary key(CustomerID);
alter table Orders add constraint fk_orders foreign key(CustomerID) references Customers(CustomerID);
*/

/*
create table OrderDetails ( OrderDetailID varchar(30) not null primary key , OrderID varchar(20), ProductID varchar(20), Quantity int, foreign key(OrderID) references Orders(OrderID), foreign key (ProductID) references Products(ProductID));
create table Inventory(InventoryID varchar(20) not null primary key, ProductID varchar(20), foreign key(ProductID) references Products(ProductID), QuantityInStock int, LastStockUpdate int);
*/

--alter database sis modify name = "TechShop";

/*insert into Customers values('101','Bobby','jostar','bobby@gmail.com','8745962130','Japan'),
							('102','Sunny','jostar','sunny@gmail.com','8745968523','South Korea'),
							('103','Brock','Lesnar','brock@gmail.com','8745969645','Australia'),
							('104','Roman','Reigns','RomanReigns@gmail.com','9645822130','France'),
							('105','Dean','Ambros','deanambros@gmail.com','6597962130','Switezerland'),
							('106','Seth','Rollings','rollings@gmail.com','4785962130','Iceland'),
							('107','Braun','Stroman','braunstroman@gmail.com','5695962130','Antatica'),
							('108','Luke','Harper','crazyluke@gmail.com','3215962130','Poland'),
							('109','Randy','Orton','Randyviper@gmail.com','5735995130','chile'),
							('110','Triple','H','hhh@gmail.com','7845962130','Canada');
*/

/*insert into Products values('fan195','fan','fan with 3 leafs',2500),
							('bucket852','bucket','steel bucket',350),
							('table354','table','wooden table',550),
							('kettle969','kettle','for water and edd boiling',650),
							('pen579','pen','blank and blue pen',60),
							('jug025','jug','plastic jug',30),
							('earphone696','earphone','wired earphones',100),
							('chair267','chair','plastic chairs',85),
							('bottle195','bottle','copper bottles',35),
							('tubelight645','tubelight','fillips tubelight',15);
*/


/*insert into Orders values('1111','101','2025-03-20',30),
							('1211','101','2025-03-20',100),
							('1311','102','2025-03-19',15),
							('1411','102','2025-03-19',25),
							('1511','103','2025-03-18',60),
							('1611','104','2025-03-17',30),
							('1711','107','2025-03-16',100),
							('1811','107','2025-03-16',85),
							('1911','109','2025-03-15',35),
							('2011','110','2025-03-14',15);
							*/
/*insert into OrderDetails values('a11','1111','fan195',30),
							('a12','1111','kettle969',100),
							('a13','1211','kettle969',15),
							('a14','1211','fan195',25),
							('a15','1311','bucket852',60),
							('a16','1411','earphone696',30),
							('a17','1711','tubelight645',100),
							('a18','1711','chair267',85),
							('a19','1911','chair267',35),
							('a20','2011','fan195',15);*/

/*insert into Inventory values('11','fan195',25,30),
							('12','bucket852',60,100),
							('13','table354',10,15),
							('14','kettle969',15,25),
							('15','bottle657',50,60),
							('16','table354',20,30),
							('17','earphone696',80,100),
							('18','chair267',60,85),
							('19','fan195',25,35),
							('20','tubelight645',7,15);*/

select * from Customers;
select * from Inventory;
select * from OrderDetails;
select * from Orders;
select * from Products;