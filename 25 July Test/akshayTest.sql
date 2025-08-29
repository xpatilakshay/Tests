-- MySQL Practical Evaluation Test
-- ⏱ Total Duration: 180 Minutes
-- 🧠 Level: Expert / Hard
-- 📦 Test Structure (4 Blocks):
-- 1. Advanced Schema Design with Constraints & Indexing
-- 2. Multi-Layer Querying & Analytical SQL
-- 3. Optimization, View Materialization, and Cost Reporting
-- 4. Advanced Procedures, Triggers, and Auditing Functions


-- ✅ Block 1: Advanced Schema Design with Constraints & Indexing (30 Minutes)
-- 📌 Objective:
-- Design a normalized schema for a large-scale corporate system, with referential integrity, composite keys, indexing strategy, and temporal fields.
-- 🛠 Tasks:
-- Create a database: enterprise_ops

CREATE DATABASE enterprise_ops;
USE enterprise_ops;

-- departments
-- - dept_id INT PRIMARY KEY AUTO_INCREMENT
-- - dept_name VARCHAR(150) UNIQUE
-- - division VARCHAR(100)
-- - created_at DATETIME DEFAULT CURRENT_TIMESTAMP

CREATE TABLE departments(
dept_id INT PRIMARY KEY AUTO_INCREMENT,
dept_name VARCHAR(150) UNIQUE,
division VARCHAR(100),
created_at DATETIME DEFAULT current_timestamp
);

INSERT INTO departments (dept_name, division) VALUES
('IT', 'Development'),
('Human Resources', 'Resources'),
('Digital Marketing', 'Marketing'),
('Finance', 'Accounting'),
('Customer Support', 'Services');


-- employees
-- - emp_id INT PRIMARY KEY AUTO_INCREMENT
-- - emp_name VARCHAR(120)
-- - email VARCHAR(150) UNIQUE
-- - salary DECIMAL(12, 2)
-- - bonus_percent DECIMAL(5,2) DEFAULT 0.00
-- - joining_date DATE
-- - active_flag BOOLEAN DEFAULT TRUE
-- - dept_id INT, FK → departments
-- - manager_id INT, FK → employees(emp_id)
-- - last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP


CREATE TABLE employees(
emp_id INT PRIMARY KEY AUTO_INCREMENT,
emp_name VARCHAR(120),
email VARCHAR(150) unique,
salary DECIMAL(12,2),
bonus_percent DECIMAL(5,2) default 0.00,
joining_date DATE,
active_flag BOOLEAN DEFAULT TRUE,
dept_id INT,
manager_id INT,
last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
FOREIGN KEY (manager_id) REFERENCES employees(emp_id)
);

INSERT INTO employees (emp_name, email, salary, bonus_percent, joining_date, dept_id, manager_id)
VALUES 
('Harshal Kambe', 'harshal.kambe@smartinfologiks.com', 65000, 7.50, '2021-01-10', 2, null);

INSERT INTO employees (emp_name, email, salary, bonus_percent, joining_date, dept_id, manager_id)
VALUES 
('Akshay Patil', 'akshay.patil@smartinfologiks.com', 5000, 10.00, '2025-07-14', 1, 16),
('Indulekha Singh', 'indulekha.singh@smartinfologiks.com', 70000.00, 12.00, '2020-11-05', 1, 16),
('Raghu shinde', 'raghu.shinde@smartinfologiks.com', 58000.00, 6.00, '2023-03-20', 3, 16),
('Amit Joshi', 'amit.joshi@smartinfologiks.com', 47000.00, 8.00, '2021-09-25', 4, 16);

select * from employees;

-- projects
-- - project_id INT PRIMARY KEY AUTO_INCREMENT
-- - project_name VARCHAR(120) UNIQUE
-- - start_date DATE
-- - end_date DATE
-- - budget DECIMAL(15, 2)
-- - status ENUM('Planning','Active','Closed')

CREATE TABLE projects(
project_id INT PRIMARY KEY AUTO_INCREMENT,
project_name VARCHAR(120) UNIQUE,
start_date DATE,
end_date DATE,
budget DECIMAL(15,2),
status ENUM('Planning','Active','Closed')
);

INSERT INTO projects (project_name, start_date, end_date, budget, status)
VALUES 
('ETuts', '2023-01-01', '2023-12-31', 1500000.00, 'Active'),
('KnowyAI', '2022-05-10', '2023-05-10', 850000.00, 'Closed'),
('Marketing Automation', '2024-02-01', '2024-12-31', 500000.00, 'Planning'),
('Customer Support Portal', '2023-06-01', '2024-06-01', 600000.00, 'Active'),
('Finance System Upgrade', '2022-08-01', '2023-08-01', 750000.00, 'Closed');

select * from projects;

-- employee_projects
-- - emp_id INT FK → employees
-- - project_id INT FK → projects
-- - hours_allocated INT
-- - assigned_on DATE DEFAULT CURRENT_DATE
-- - Composite PK: (emp_id, project_id)

CREATE TABLE employee_projects (
    emp_id INT,
    project_id INT,
    hours_allocated INT,
    assigned_on DATE,
    PRIMARY KEY (emp_id, project_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

INSERT INTO employee_projects (emp_id, project_id, hours_allocated, assigned_on)
VALUES
(37, 1, 120, DEFAULT),
(16, 2, 100, DEFAULT),
(38, 1, 150, DEFAULT),
(39, 3, 90, DEFAULT),
(40, 4, 110, DEFAULT);

select * from employee_projects;

DELIMITER //

CREATE TRIGGER set_assigned_date
BEFORE INSERT ON employee_projects
FOR EACH ROW
BEGIN
    IF NEW.assigned_on IS NULL THEN
        SET NEW.assigned_on = CURDATE();
    END IF;
END;
//

DELIMITER ;


-- Indexing Requirements:
-- - Composite index on (dept_id, joining_date)
-- - Index on projects(status, start_date)
-- - Index on employee_projects(hours_allocated)
-- - Use FULLTEXT on projects.project_name

CREATE INDEX idx_emp_dept_join ON employees(dept_id, joining_date);
CREATE INDEX idx_proj_status_date ON projects(status, start_date);
CREATE INDEX idx_ep_hours ON employee_projects(hours_allocated);
CREATE FULLTEXT INDEX idx_project_name_ft ON projects(project_name);


-- ✅ Block 2: Multi-Layer Querying & Analytical SQL (45 Minutes)
-- 📌 Objective:

-- Write advanced and layered queries using CTEs, subqueries, correlated subqueries, window functions, and dynamic filters.
--     1. 1. Get the top 3 most expensive projects (by total employee cost: hours_allocated * salary) 
			-- using a window function and partition by status.

SELECT project_name,p.status,sum(ep.hours_allocated * e.salary) as "Total Cost" from projects p 
JOIN employee_projects ep ON p.project_id = ep.project_id
JOIN employees e ON e.emp_id = ep.emp_id
GROUP BY p.project_id, p.status
order by sum(ep.hours_allocated * e.salary) desc limit 3;

	
--  2. 2. List employees who joined in the last 2 years, are not assigned to any Active or Planning project, 
	  -- and have bonus > avg department bonus.
      
select e.emp_id,e.emp_name from employees e join employee_projects ep 
on e.emp_id = ep.emp_id join projects p on ep.project_id = p.project_id
where e.joining_date >= CURDATE() - INTERVAL 2 YEAR and p.status not in ("Active","Planning");

--     3. 3. For each department, show: total employees, number of inactive employees, highest salary, and variance in salary using VARIANCE().

select dept_name,sum(CASE WHEN e.active_flag = 0 THEN 1 ELSE 0 END) as "Inactive Employees",max(e.salary),variance(salary) from departments d join 
employees e on e.dept_id=d.dept_id group by dept_name; 

--     4. 4. List managers who have more than 5 direct reports and at least 2 reports working on more than 3 projects.

select e.manager_id from employees e group by e.manager_id having count(e.emp_id)>5
and sum((SELECT count(*) FROM employee_projects ep where ep.emp_id = e.emp_id) > 3) >= 2;

--     5. 5. Using CTEs, build a timeline report: Project ID, Name, Duration (in days), Allocated Hours, Employee Count (Active projects started in last 365 days).

with active_recent_projects AS ( select project_id, project_name, DATEDIFF(end_date, start_date) as duration
from projects
where status = 'Active' and start_date >= CURDATE() - INTERVAL 365 DAY) select 
p.project_id, p.project_name, p.duration,
COALESCE(SUM(ep.hours_allocated), 0) AS allocated_hours,
COUNT(DISTINCT ep.emp_id) AS employee_count
FROM active_recent_projects p
LEFT JOIN employee_projects ep ON p.project_id = ep.project_id
GROUP BY p.project_id;



-- ✅ Block 3: Optimization, View Materialization, and Reporting (35 Minutes)
-- 📌 Objective:
-- Use views, materialization, and query analysis to build enterprise-level reports and optimize heavy queries.
--     6. 1. Create a view department_performance_summary with dept_id, total_salary, avg_bonus, 
       -- employee_count, projects_count (for departments with > 5 employees).
      
create view department_performance_summary as select d.dept_id,
sum(e.salary) as total_salary,
avg(e.salary * e.bonus_percent) as avg_bonus,
count(e.emp_id) as employee_count,
count(distinct ep.project_id) as projects_count
from departments d
join employees e on d.dept_id = e.dept_id
left join employee_projects ep on e.emp_id = ep.emp_id
group by d.dept_id
having employee_count > 5;

--     7. 2. Create a materialized summary table project_summary with project_id, project_name, total_hours, cost_estimate, 
       -- remaining_budget, last_synced. Write SQL to refresh daily.
       
	create table project_summary (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(120),
    total_hours INT,
    cost_estimate DECIMAL(15,2),
    remaining_budget DECIMAL(15,2),
    last_synced DATETIME DEFAULT CURRENT_TIMESTAMP
);


--     8. 3. Pick your most expensive query from Block 2, run EXPLAIN ANALYZE, identify index usage and recommend changes.

--  i choose this Get the top 3 most expensive projects (by total employee cost: hours_allocated * salary) using a window function and partition by status.

Explain SELECT project_name,p.status,sum(ep.hours_allocated * e.salary) as "Total Cost" from projects p 
JOIN employee_projects ep ON p.project_id = ep.project_id
JOIN employees e ON e.emp_id = ep.emp_id
GROUP BY p.project_id, p.status
order by sum(ep.hours_allocated * e.salary) desc limit 3;

-- In this this query has runned quicker than normal query without index as index has been assigned to multiple coulums so it becomes quicker to fetch data by index

--     9. 4. Create a pivot-style report using conditional aggregation: show count of employees in each bonus range (0–5%, 5–10%, >10%) for each department.

select d.dept_id,d.dept_name,
count(case when e.bonus_percent>=0 and e.bonus_percent<=5 then 1 end) as "Between 0 and 5",
count(case when e.bonus_percent>5 and e.bonus_percent<=10 then 1 end) as "Between 5 and 10",
count(case when e.bonus_percent>10 then 1 end) as "Greater than 10"
from departments d join employees e on d.dept_id = e.dept_id
group by dept_id order by d.dept_id;

-- ✅ Block 4: Advanced Procedures, Triggers, and Auditing Functions (70 Minutes)
-- 📌 Objective:
-- Implement robust business logic and automation using MySQL's stored routines and triggers.
--     10. 1. Stored Procedure: restructure_department - Moves employees based on salary and logs changes into dept_transfer_log.

create table dept_transfer_log(
emp_id int,
old_dept_name varchar(100),
new_dept_name varchar(100),
old_salary decimal(12,2),
new_salary decimal(12,2)
);


delimiter //
create procedure restructure_department(in emp_id int)
begin
	insert into dept_transfer_log(emp_id,old_dept_name,new_Dept_name,old_salary,new_Salary) values
    (old.emp_id,old.dept_name,new.dept_name,old.salary,new.salary);
end//
delimiter ;


--     11. 2. Trigger: prevent_overbudget_assignment - Checks total cost before INSERT into employee_projects and blocks if it exceeds project budget.

DELIMITER //
create trigger prevent_overbudget_assignment
before insert on employee_projects
for each row
BEGIN
    declare total_cost DECIMAL(15,2);
    declare proj_budget DECIMAL(15,2);

    select budget into proj_budget from projects where project_id = new.project_id;
    select sum(hours_allocated*salary) into proj_budget from employees; 

    if total_cost>proj_budget then 
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Assignment exceeds project budget';
    END IF;
END//
DELIMITER ;

--     12. 3. Function: get_employee_earnings(emp_id INT) - Calculates total earnings from project assignments including bonus multiplier.

delimiter //
create function get_employee_earnings(emp_id int)
returns decimal(12,2)
deterministic
begin
declare total decimal(12,2);
select sum(ep.hours_allocated * e.salary * (1 + e.bonus_percent / 100))
into total
from employee_projects ep
join employees e on ep.emp_id = e.emp_id
where ep.emp_id = emp_id;
return ifnull(total, 0);
end;
//
delimiter ;



--     13. 4. Audit Trigger: AFTER UPDATE on employees logs salary and bonus changes into employee_audit_log.

create table employee_audit_log(
emp_id int,
old_salary decimal(12,2),
new_Salary decimal(12,2),
old_bonus decimal(5,2),
new_bonus decimal(5,2),
changed_on timestamp default current_timestamp
);


delimiter //
create trigger employee_audit_log
after update on employees
for each row 
begin
	if old.salary != new.salary and old.bonus_percent != new.bonus_percent then
		insert into employee_audit_log(emp_id,old_salary,new_salary,old_bonus,new_bonus)
        values (old.emp_id,old.salary,new.salary,old.bonus_percent,new.bonus_percent);
    end if;
end//

delimiter ;
