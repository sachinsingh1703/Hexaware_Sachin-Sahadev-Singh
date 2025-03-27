use techshop;

--1
select firstname, lastname, email 
from customers;

--2
select o.orderid, o.orderdate, c.firstname, c.lastname 
from orders o
join customers c on o.customerid = c.customerid;

--3
insert into customers (firstname, lastname, email, phone, address)
values ('seth', 'rollins', 'seth.rollins@wwe.com', '9998887781', '999 kingslayer lane, usa');

--4
update products
set price = price * 1.10
where productname like '%electronics%';

--5
declare @orderid int = 3005;

delete from orderdetails where orderid = @orderid;
delete from orders where orderid = @orderid;

--6
insert into orders (customerid, orderdate, totalamount)
values (1002, getdate(), 79.99);

--7
declare @customerid int = 1003;
declare @newemail nvarchar(100) = 'xyz@wwe.com';
declare @newaddress nvarchar(255) = 'pani kai piche wala area, usa';

update customers
set email = @newemail, address = @newaddress
where customerid = @customerid;

--8
update orders
set totalamount = coalesce((
    select sum(p.price * od.quantity)
    from orderdetails od
    join products p on od.productid = p.productid
    where od.orderid = orders.orderid
), 0);


--9
declare @customerid int = 1004;

delete from orderdetails where orderid in (select orderid from orders where customerid = @customerid);
delete from orders where customerid = @customerid;


--10
insert into products (productname, description, price)
values ('wwe titantron speaker', 'bluetooth speaker with wwe entrance themes', 129.99);


--11
alter table orders add status nvarchar(50) default 'pending'; -- run once to add status column if it doesn't exist

declare @orderid int = 3012;
declare @newstatus nvarchar(50) = 'shipped';

update orders
set status = @newstatus
where orderid = @orderid;


--12
alter table customers add ordercount int default 0;

update customers
set ordercount = (
    select count(*)
    from orders o
    where o.customerid = customers.customerid
);


