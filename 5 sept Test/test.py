# Evaluation Exam – Python & MySQL

# Section A – Python (50 Marks)

'''Q1. File Parsing & Data Transformation (12 Marks)
Given a CSV file sales.csv with the format:
OrderID, CustomerName, Product, Quantity, Price
101, Rajesh, Laptop, 2, 45000
102, Anita, Mobile, 5, 15000
103, Sameer, Laptop, 1, 46000
104, Meena, Tablet, 3, 20000

Tasks:
- Load into dictionary of lists.
- Compute total sales per customer.
- Save results into customer_sales.json'''

import csv
import json

data_dict = {}
with open("sales.csv", "r") as file:
    reader = csv.DictReader(file)
    for key in reader.fieldnames:
        data_dict[key] = []
    for row in reader:
        for key in reader.fieldnames:
            if key in ["Quantity", "Price"]:
                data_dict[key].append(int(row[key]))
            else:
                data_dict[key].append(row[key])

customer_sales = {}
for i in range(len(data_dict['CustomerName'])):
    customer = data_dict['CustomerName'][i]
    total = data_dict['Quantity'][i] * data_dict['Price'][i]
    if customer in customer_sales:
        customer_sales[customer] += total
    else:
        customer_sales[customer] = total

with open("customer_sales.json", "w") as f:
    json.dump(customer_sales, f, indent=4)

print("Customer sales saved to customer_sales.json")



'''Q2. Advanced Functions & Generators (10 Marks)
Create generator prime_generator(n) that yields primes up to n.
- Generate primes up to 200.
- Filter only palindrome primes.'''

def prime_generator(n):
    sieve = [True] * (n+1)
    sieve[0:2] = [False, False]
    for i in range(2, n+1):
        if sieve[i]:
            yield i
            for j in range(i*i, n+1, i):
                sieve[j] = False

primes = list(prime_generator(200))

palindrome_primes = [p for p in primes if str(p) == str(p)[::-1]]
print("Palindrome primes up to 200:", palindrome_primes)



'''Q3. OOP with Inheritance & Polymorphism (12 Marks)
Class Hierarchy:
- Employee(emp_id, name, salary)
- Manager(bonus)
- Developer(programming_language)
Override calculate_salary().
Create objects, store in list, print via polymorphism.'''


class Employee:
    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary
    
    def calculate_salary(self):
        return self.salary
    
    def __str__(self):
        return f"{self.name}: {self.calculate_salary()}"

class Manager(Employee):
    def __init__(self, emp_id, name, salary, bonus):
        super().__init__(emp_id, name, salary)
        self.bonus = bonus
    
    def calculate_salary(self):
        return self.salary + self.bonus

class Developer(Employee):
    def __init__(self, emp_id, name, salary, programming_language):
        super().__init__(emp_id, name, salary)
        self.programming_language = programming_language

employees = [
    Manager(1, "Rajesh", 80000, 15000),
    Developer(2, "Anita", 60000, "Python"),
    Employee(3, "Sameer", 50000)
]

for emp in employees:
    print(emp)



'''Q4. Python-MySQL Data Migration (16 Marks)
- Connect to MySQL (CompanyDB).
- Fetch employees with salary > 50,000.
- Store results in Pandas DataFrame.
- Export to high_salary_employees.csv.
- Handle DB connection & query errors.'''


import mysql.connector
import pandas as pd

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="akshay",
        database="test"
    )
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM employee WHERE salary > 50000"
    cursor.execute(query)
    results = cursor.fetchall()
    

    df = pd.DataFrame(results)
    

    df.to_csv("high_salary_employees.csv", index=False)
    print("High salary employees exported to high_salary_employees.csv")

except mysql.connector.Error as e:
    print("Database error:", e)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()


