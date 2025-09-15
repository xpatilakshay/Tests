-- MySQL Practical Exam
-- Section A – Joins (30 Marks)

CREATE DATABASE twelve_sept;
USE twelve_sept;

-- 1. Inner Join Task (10 Marks)
-- - You have two tables:
--  - employees(emp_id, emp_name, dept_id, salary)
--  - departments(dept_id, dept_name)
-- - Write a query to display all employee names, their department names, and salaries.

CREATE TABLE employees(
emp_id INT, 
emp_name VARCHAR(50), 
dept_id INT, 
salary DECIMAL(10,2)
);

INSERT INTO employees (emp_id, emp_name, dept_id, salary) 
VALUES
(1,"Akshay",1,30000),
(2,"Harshal",1,70000),
(3,"Rohan",2,50000),
(4,"Sanket",3,60000),
(5,"Rajesh",3,"34000");

ALTER TABLE employees ADD COLUMN manager_id int;

INSERT INTO employees (manager_id) values 
(2),(2),(2),(1),(1);

update employees set emp_id = 6 where emp_name="Vaibhav";

select * from employees;

INSERT INTO employees (emp_id, emp_name, dept_id, salary) 
VALUES
(5,"Vaibhav",NULL,70000);


CREATE TABLE departments(dept_id int, dept_name VARCHAR(50));

INSERT INTO departments(dept_id, dept_name) 
VALUES
(1,"IT"),
(2,"HR"),
(3,"Digital Marketing");


SELECT e.emp_name, d.dept_name, e.salary
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;


-- 2. Left Join Task (10 Marks)
-- - Some employees may not be assigned to a department.
-- - Write a query to display all employees along with department names (if available). Show
-- 'No Department' if none.

SELECT e.emp_name,
coalesce(d.dept_name,"No Department") as dept_name
from employees e LEFT JOIN
departments d ON 
e.dept_id = d.dept_id;


-- 3. Self Join Task (10 Marks)
-- - Assume employees also has a column manager_id referring to another emp_id.
-- - Write a query to display each employee’s name along with their manager’s name.

SET SQL_SAFE_UPDATES = 0;
DELETE FROM employees WHERE emp_name IS NULL;

UPDATE employees SET manager_id = 2 WHERE emp_id IN (1,3,4);
UPDATE employees SET manager_id = 1 WHERE emp_id IN (5,6); 

SELECT 	
e.emp_name AS employee,
m.emp_name AS manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.emp_id;


-- Section B – Stored Procedures (20 Marks)
-- 4. Procedure Creation (10 Marks)
-- - Write a stored procedure GetEmployeeDetails(IN deptName VARCHAR(50)) that returns
-- all employee names, salaries, and department names for the given department.

DELIMITER //

CREATE PROCEDURE GetEmployeeDetails(IN deptName VARCHAR(50))
BEGIN
    SELECT e.emp_name, e.salary, d.dept_name
    FROM employees e
    INNER JOIN departments d ON e.dept_id = d.dept_id
    WHERE d.dept_name = deptName;
END //

DELIMITER ;

CALL GetEmployeeDetails('IT');



-- 5. Procedure with Condition (10 Marks)
-- - Write a stored procedure IncreaseSalary(IN deptName VARCHAR(50), IN percentage
-- DECIMAL(5,2)) that increases the salary of all employees in the given department by the
-- specified percentage.



DELIMITER //

CREATE PROCEDURE IncreaseSalary(IN deptName VARCHAR(50), IN percentage DECIMAL(5,2))
BEGIN

UPDATE employees e  
INNER JOIN departments d ON e.dept_id = d.dept_id 
set e.salary = e.salary+(e.salary*(percentage/100))
where d.dept_name = deptName;

END //

DELIMITER ;




CALL IncreaseSalary('IT', 15.00);


-- Section C – Indexing (20 Marks)
-- 6. Index Usage (10 Marks)
-- - A table orders(order_id, customer_id, order_date, amount) has millions of rows.
-- - Write a query to create an index to improve performance when searching by customer_id
-- and order_date.

Create index customer_orders_index on orders(customer_id,order_date);


-- 7. Index Impact (10 Marks)
-- - Explain (with SQL queries):
--  1. How you would check if an index is being used for a query.

-- Answer ------->>>

-- In MySQL, we use the EXPLAIN (or EXPLAIN ANALYZE in newer versions) keyword before our query.

-- Example:

EXPLAIN
SELECT order_id, amount
FROM orders
WHERE customer_id = 101
AND order_date = '2025-09-01';

-- Key Points : 
-- MySQL will show the execution plan.
-- Look at the key column in the output:
-- If it shows customer_orders_index → the index is being used.
-- If it’s NULL → the index is not being used.


--  2. Why too many indexes can reduce performance.

-- Answer ------->>>

-- Indexes speed up reads, but they slow down writes (INSERT, UPDATE, DELETE).

-- Reasons:

-- Every time you modify data, all relevant indexes must also be updated.

-- More indexes is equals to mmore overhead on writes.

-- Unused indexes still consume disk space and memory.

-- The optimizer may also take longer to decide which index to use if there are too many.


-- Section D – Advanced Select Queries (30 Marks)

CREATE TABLE orders(
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),
    order_date DATE,
    amount DECIMAL(10,2)
);


INSERT INTO orders (order_id, customer_id, customer_name, order_date, amount) VALUES
(1, 101, 'Akshay',  '2025-01-05', 5000.00),
(2, 101, 'Akshay',  '2025-02-10', 12000.00),
(3, 102, 'Sahil',   '2025-01-15', 8000.00),
(4, 102, 'Sahil',   '2025-03-20', 15000.00),
(5, 103, 'Harshal', '2025-02-05', 3000.00),
(6, 103, 'Harshal', '2025-03-25', 7000.00),
(7, 104, 'Yashraj', '2025-04-10', 25000.00),
(8, 105, 'Arun',    '2025-04-15', 9500.00),
(9, 105, 'Arun',    '2025-05-01', 11000.00),
(10, 106, 'Ishwar', '2025-05-05', 4500.00),
(11, 107, 'Aniket', '2025-05-10', 13000.00);


-- 8. Aggregation with Group By (10 Marks)
-- - From the orders table, write a query to display each customer’s total order amount,
-- average order amount, and number of orders.

SELECT customer_id,customer_name,SUM(amount) AS total_order_amount,
AVG(amount) AS average_order_amount,
COUNT(order_id) AS number_of_orders
FROM orders
GROUP BY customer_id, customer_name;


-- 9. Subquery with EXISTS (10 Marks)
-- - Write a query to list all customers who have placed at least one order above ₹ 10,000. 

SELECT DISTINCT o.customer_id, o.customer_name
FROM orders o
WHERE EXISTS (
SELECT 1
FROM orders o2
WHERE o2.customer_id = o.customer_id
AND o2.amount > 10000
);


-- 10. Window Functions (10 Marks)
-- - From the employees table, write a query to display each employee’s name, department,
-- salary, and their rank within the department based on salary (highest salary = rank 1).

SELECT e.emp_name,d.dept_name,e.salary,RANK() OVER (PARTITION BY d.dept_name ORDER BY e.salary DESC) AS salary_rank
FROM employees e join departments d on e.dept_id=d.dept_id;
