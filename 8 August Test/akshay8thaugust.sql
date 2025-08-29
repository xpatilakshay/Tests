-- 8th August 2025 Test

Create database test;
use test;

-- Section A – MySQL Practical (40 marks)

-- 1. Database Setup & Normalization (5 marks)
-- - Create normalized tables for an e-commerce order system:
--   customers(customer_id, name, email, city)
-- - Define primary keys, foreign keys, and indexes for optimal performance.


create table customers(
customer_id int primary key auto_increment,
name varchar(100) not null,
email varchar(100) unique,
city varchar(50),
index idx_city (city)
);

INSERT INTO customers (name, email, city) VALUES
('Akshay Patil', 'akshay.patil@example.com', 'Kolhapur'),
('sahil Patil', 'sahil.patil@example.com', 'Mumbai'),
('Ajay Jadhav', 'ajay.jadhav@example.com', 'Nashik'),
('Priya Kulkarni', 'priya.kulkarni@example.com', 'Nagpur'),
('Vikram Shinde', 'vikram.shinde@example.com', 'Aurangabad'),
('Meera Gawande', 'meera.gawande@example.com', 'Solapur'),
('Sanjay Pawar', 'sanjay.pawar@example.com', 'Kolhapur'),
('Akash More', 'akash.more@example.com', 'Thane');


--   orders(order_id, customer_id, order_date, amount)

Create table orders(
order_id int primary key auto_increment,
customer_id int,
order_date date,
amount decimal(10,2),
foreign key (customer_id) references customers(customer_id),
index idx_orderdate (order_date),
index idx_customer_id (customer_id)
);


INSERT INTO orders (customer_id, order_date, amount) VALUES
(1, '2025-08-01', 1500.00),
(2, '2025-08-02', 2450.50),
(3, '2025-08-03', 3200.75),
(1, '2025-08-05', 1800.25),
(4, '2025-08-04', 980.00),
(5, '2025-08-06', 2150.00),
(6, '2025-08-06', 1350.40),
(7, '2025-08-07', 1750.60);


--   order_items(item_id, order_id, product_name, quantity, price)

create table order_items(
item_id int primary key auto_increment,
order_id int,
product_name varchar(100),
quantity int,
price decimal(10,2),
foreign key (order_id) references orders(order_id),
index idx_order_id (order_id) 
);

INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(1, 'Basmati Rice 5kg', 1, 750.00),
(1, 'Toor Dal 1kg', 2, 375.00),
(2, 'Sunflower Oil 1L', 3, 250.00),
(2, 'Wheat Flour 10kg', 1, 700.50),
(3, 'Masala Mix Pack', 2, 800.00),
(3, 'Sugar 5kg', 1, 400.75),
(4, 'Chitale Bhakarwadi', 4, 450.25),
(5, 'Alphonso Mango Box', 1, 980.00),
(6, 'Kokum Syrup Bottle', 2, 1075.00),
(7, 'Poha Pack 500g', 3, 450.00),
(8, 'Groundnut Oil 1L', 2, 875.30);

select * from customers;
select * from orders;
select * from order_items;

-- 2. Complex Query – Top Customers Per City (7 marks)
-- - Write a single query to find top 3 customers per city based on total amount spent in the last 12 months.

select customer_id, name, city, total_amount_spend from 
(
select c.name, c.customer_id, c.city, sum(o.amount) as total_amount_spend ,
rank() over (partition by city order by sum(o.amount) desc) as ranking
from customers c join orders o on c.customer_id = o.customer_id
where o.order_date >= curdate() - interval 12 month
group by c.customer_id,c.name,c.city
) as ranked 
where ranking<=3
order by total_amount_spend desc limit 3;


-- 3. Duplicate Removal (5 marks)
-- - In the orders table, delete duplicate rows keeping only the record with the smallest order_id for each (customer_id, order_date).
SET SQL_SAFE_UPDATES = 0;
delete ord1 from orders ord1 join orders ord2 on ord1.customer_id = ord2.customer_id and ord1.order_date = ord2.order_date;  

-- 4. Pivot Report (8 marks)
-- - Create a query to display total orders per month for 2024, showing months as columns.

select 
count(case when month(order_date) = 1 then 1 end ) as january,
count(case when month(order_date) = 2 then 1 end ) as February,
count(case when month(order_date) = 3 then 1 end ) as March,
count(case when month(order_date) = 4 then 1 end ) as April,
count(case when month(order_date) = 5 then 1 end ) as May,
count(case when month(order_date) = 6 then 1 end ) as June,
count(case when month(order_date) = 7 then 1 end ) as July,
count(case when month(order_date) = 8 then 1 end ) as August,
count(case when month(order_date) = 9 then 1 end ) as September,
count(case when month(order_date) = 10 then 1 end ) as octomber,
count(case when month(order_date) = 11 then 1 end ) as november,
count(case when month(order_date) = 12 then 1 end ) as december
from orders where order_date >= "2024-1-1" and order_date<"2025-1-1";

-- 5. Query Optimization (7 marks)
-- - You are given the query:
-- SELECT * FROM orders WHERE YEAR(order_date) = 2024 AND amount > 500 ORDER BY order_date DESC;
-- - Rewrite it for maximum efficiency using indexes and avoiding functions on indexed columns.

create index idx_ord_amount on 
orders(order_Date,amount);

select * from orders where order_date>="2024-1-1" and order_date<"2025-1-1" and amount>500 order by order_date desc;

-- 6. Trigger Implementation (8 marks)
-- - Create a MySQL trigger that automatically logs all deleted orders into a table deleted_orders with columns: (order_id, deleted_at, deleted_by).

create table deleted_orders(
order_id int,
deleted_at datetime,
deleted_by varchar(100)
);


delimiter //
create trigger after_delete_logger
After delete on orders
for each row
begin
insert into deleted_orders(order_id,deleted_at,deleted_by) values (old.order_id,now(),current_user);
end //
delimiter ;

select * from orders;


