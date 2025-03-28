use techshop;

--1
select o.orderid, o.orderdate, c.firstname, c.lastname, c.email, c.phone
from Orders o
join Customers c on o.customerid = c.customerid;

--2
select p.productname, sum(od.quantity * p.price) as total_revenue
from orderdetails od
join products p on od.productid = p.productid
where p.productname like '%shirt%'
group by p.productname
order by total_revenue desc;

--3
select c.firstname, c.lastname, c.email, c.phone
from customers c
join orders o on c.customerid = o.customerid
group by c.firstname, c.lastname, c.email, c.phone;

--4
select top 1 p.productname, sum(od.quantity) as total_quantity_ordered
from orderdetails od
join products p on od.productid = p.productid
where p.productname like '%shirt%'
group by p.productname
order by total_quantity_ordered desc;

--5
select productname, description
from products
where description like '%tee%';

--6
select c.firstname, c.lastname, avg(o.totalamount) as avg_order_value
from orders o
join customers c on o.customerid = c.customerid
group by c.firstname, c.lastname
order by avg_order_value desc;

--7
select top 1 o.orderid, c.firstname, c.lastname, o.totalamount
from orders o
join customers c on o.customerid = c.customerid
order by o.totalamount desc;

--8
select p.productname, count(od.orderid) as times_ordered
from orderdetails od
join products p on od.productid = p.productid
where p.productname like '%shirt%'
group by p.productname
order by times_ordered desc;

--9
declare @product_name nvarchar(255) = 'wwe titantron speaker';

select distinct c.firstname, c.lastname, c.email, c.phone
from customers c
join orders o on c.customerid = o.customerid
join orderdetails od on o.orderid = od.orderid
join products p on od.productid = p.productid
where p.productname = @product_name;


--10
declare @start_date date = '2024-01-01';
declare @end_date date = '2024-12-31';

select sum(totalamount) as total_revenue
from orders
where orderdate between @start_date and @end_date;
