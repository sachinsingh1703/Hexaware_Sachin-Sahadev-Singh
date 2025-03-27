use techshop;

--1
select firstname, lastname, email, phone
from customers
where customerid not in (select distinct customerid from orders);

--2
select count(*) as total_products
from products;

--3
select sum(totalamount) as total_revenue
from orders;

--4
declare @category_name nvarchar(255) = '%shirt%';

select (
    select avg(quantity) 
    from orderdetails 
    where productid in (select productid from products where description like @category_name)
) as avg_quantity_ordered;

--5
declare @customer_id int = 1002;

select sum(totalamount) as total_spent
from orders
where customerid = @customer_id;

--6
select top 1 c.firstname, c.lastname, count(o.orderid) as total_orders
from customers c
join orders o on c.customerid = o.customerid
group by c.firstname, c.lastname
order by total_orders desc;

--7
select top 1 p.description, sum(od.quantity) as total_quantity_ordered
from orderdetails od
join products p on od.productid = p.productid
group by p.description
order by total_quantity_ordered desc;

--8
select top 1 c.firstname, c.lastname, sum(od.quantity * p.price) as total_spent
from customers c
join orders o on c.customerid = o.customerid
join orderdetails od on o.orderid = od.orderid
join products p on od.productid = p.productid
where p.description like '%shirt%'
group by c.firstname, c.lastname
order by total_spent desc;


--9
select (
    (select sum(totalamount) from orders) / 
    (select count(*) from orders)
) as avg_order_value;


--10
select c.firstname, c.lastname, count(o.orderid) as order_count
from customers c
left join orders o on c.customerid = o.customerid
group by c.firstname, c.lastname
order by order_count desc;
