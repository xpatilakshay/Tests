# Section 1: Core Python (Coding Tasks)
'''Q1. File Handling & Data Processing
You are given a log file `server.log` with entries like:
2025-09-24 10:05:23, INFO, User=harshal, Action=Login
2025-09-24 10:15:40, ERROR, User=manish, Action=PaymentFailed
2025-09-24 10:25:10, INFO, User=suvarna, Action=Logout
Write a Python script to:
1. Count total number of `ERROR` logs.
2. Extract unique users who have logged in.
3. Save the results in a JSON file (`result.json`).'''
import json
error_count=0
login_users = set()
with open("server.log","r") as file:
    for line in file:
        if "ERROR" in line.strip():
            error_count+=1
        if "Action=Login" in line.strip():
            parts = line.split(",")
            for part in parts:
                if "User=" in part:
                    user = part.split("=")[1].strip()
                    login_users.add(user)
result = {
    "error_count":error_count,
    "login_users":list(login_users)
}

with open("result.json","w") as json_file:
    json.dump(result,json_file,indent=4)
    print("JSON file generated successfully for logged in users")



'''Q2. OOP & Inheritance
Create a class `Employee` with attributes `name`, `salary`, and `department`.
- Add a method to display employee details.
- Create a subclass `Developer` with an extra attribute `programming_language`.
- Create another subclass `Tester` with an extra attribute `testing_tool`.
- Instantiate objects for both classes and display details.'''
 
class Employee:
    def __init__(self, name, salary, department):
        self.name = name
        self.salary = salary
        self.department = department

    def employee_details(self):
        print(f"Employee Name      : {self.name}")
        print(f"Employee Salary    : {self.salary}")
        print(f"Employee Department: {self.department}")


class Developer(Employee):
    def __init__(self, name, salary, department, programming_language):
        super().__init__(name, salary, department)
        self.programming_language = programming_language

    def employee_details(self):
        super().employee_details()
        print(f"Programming Language: {self.programming_language}")


class Tester(Employee):
    def __init__(self, name, salary, department, testing_tool):
        super().__init__(name, salary, department)
        self.testing_tool = testing_tool

    def employee_details(self):
        super().employee_details()
        print(f"Testing Tool       : {self.testing_tool}")



dev = Developer("Akshay", 35000, "IT", "Python")
print("Developer Details:")
dev.employee_details()
print()

test = Tester("Yashraj", 40000, "IT", "Selenium")
print("Tester Details:")
test.employee_details()



'''Q3. Exception Handling & Debugging
The following code has multiple issues. Fix them and make it work properly:
def divide(a, b):
 return a/b
numbers = [(10, 2), (5, 0), ("8", 4)]
for x, y in numbers:
 print(f"Result: {divide(x, y)}")
Expected output:
Result: 5.0
Error: Division by zero
Error: Invalid input types'''


def divide(a, b):
    return a / b

numbers = [(10, 2), (5, 0), ("8", 4)]

for x, y in numbers:
    try:
        result = divide(x, y)
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: Division by zero")
    except TypeError:
        print("Error: Invalid input types")


# Section 2: Data Handling & Libraries
'''Q4. Pandas Data Analysis
Given a CSV file `sales.csv` with the following columns:
`Date, Product, Quantity, Price`
Tasks:
1. Load the CSV using pandas.
2. Find the total revenue per product.
3. Find the best-selling product (by quantity).
4. Save results to `sales_summary.csv`.'''

import pandas as pd

df = pd.read_csv("sales.csv")

df["revenue"] = df["Quantity"]*df["Price"]
total_revenue = df.groupby("Product")["revenue"].sum()
product_quantity = df.groupby("Product")["Quantity"].sum()
best_selling_product = product_quantity.idxmax()
best_selling_quantity = product_quantity.max() 
summary = pd.DataFrame(
    {
        "Total Revenue":total_revenue,
        "Total Quantity Sold":product_quantity
    }
)
summary.to_csv("sales_summary.csv")


print(summary)
print(f"Best selling product is '{best_selling_product}' with {best_selling_quantity} units sold.")


'''Q5. API Integration
Write a Python script that fetches data from this API:
https://jsonplaceholder.typicode.com/posts
- Print the title of all posts written by `userId=1`.
- Save the filtered posts to `user1_posts.json`.'''

import requests
import json


url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

if response.status_code == 200:
    posts = response.json()

    user1_posts = [post for post in posts if post["userId"] == 1]

    print("Title of the posts by userId=1")
    for post in user1_posts:
        print(post["title"])

    with open("user1_posts.json","w") as file:
        json.dump(user1_posts,file,indent=4)
    
    print("\nFiltered posts saved to 'user1_posts.json'.")

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


# Section 3: Advanced Concepts
'''Q6. Decorators
Create a decorator `time_logger` that measures and prints the execution time of any
function.
- Use it on a function that calculates the sum of numbers from 1 to 1,000,000.'''

import time

def time_logger(func):
    def wrapper(*args, **kwargs):
        start_time = time.time() 
        result = func(*args, **kwargs)
        end_time = time.time()    
        print(f"Execution time of '{func.__name__}': {end_time - start_time:.6f} seconds")
        return result
    return wrapper


@time_logger
def sum_numbers():
    return sum(range(1, 1_000_001))

total = sum_numbers()
print(f"Sum: {total}")



'''Q7. Generators
Write a generator function `fibonacci(n)` that yields the first `n` Fibonacci numbers.
- Print the first 10 numbers using the generator.'''

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)



'''Q8. Database Handling
Using sqlite3:
- Create a database `company.db` with a table `employees(id, name, role, salary)`.
- Insert 3 employee records.
- Write a query to fetch all employees with salary > 50,000.'''


import sqlite3

conn = sqlite3.connect('company.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    salary REAL NOT NULL
)
''')

employees = [
    (1, 'Akshay', 'Developer', 60000),
    (2, 'Harshal', 'Designer', 45000),
    (3, 'Sagar', 'Manager', 75000)
]

cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?)', employees)

conn.commit()

cursor.execute('SELECT * FROM employees WHERE salary > 50000')
high_salary_employees = cursor.fetchall()

print("Employees with salary > 50,000:")
for emp in high_salary_employees:
    print(emp)

conn.close()



# Section 4: Problem-Solving
'''Q9. Algorithm
Write a function `two_sum(nums, target)` that returns indices of two numbers in the list
`nums` that add up to the given `target`.
Example:
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))'''

def two_sum(nums, target):
    seen = {}  
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target)) 


'''Q10. Real-World Task
Write a script that:
1. Reads a text file `input.txt`.
2. Removes all stopwords (`the, is, in, and, of, to, a`).
3. Counts the frequency of each remaining word.
4. Saves the top 5 most frequent words in `output.txt`.'''

from collections import Counter

stopwords = {'the', 'is', 'in', 'and', 'of', 'to', 'a'}

with open('input.txt', 'r', encoding='utf-8') as file:
    text = file.read().lower() 

words = [word.strip('.,!?') for word in text.split() if word not in stopwords]

word_counts = Counter(words)

top5 = word_counts.most_common(5)

with open('output.txt', 'w', encoding='utf-8') as out_file:
    for word, freq in top5:
        out_file.write(f"{word}: {freq}\n")

print("Top 5 words saved to output.txt")
