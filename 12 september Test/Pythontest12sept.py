# Python Practical Exam
# Section A – Core Python (25 Marks)
'''

1. Functions (10 Marks)
- Write a Python function is_prime(n) that checks if a number is prime.
- Then, write another function prime_in_range(start, end) that returns a list of all prime 
numbers between start and end.

'''

def is_prime(n):
    if n<2:
        return False
    for i in range (2, int(n**0.5)+1):
        if n%i==0:
            return False
    return True

def prime_in_range(start, end):
    primes = []
    for num in range(start, end+1):
        if is_prime(num):
            primes.append(num)
    return primes

print(prime_in_range(10, 50))

'''
2. String & List Operations (15 Marks)
- Given a string: "openAI develops AI tools in Python".
- Write a program to:
  1. Count how many times each word appears.
  2. Reverse the order of words.
  3. Display the unique words in sorted order.
'''

sentence = "openAI develops AI tools in Python"
words = sentence.split()
word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1
print("Word Count:", word_count)

reversed_words = ' '.join(reversed(words))
print("Reversed Words:", reversed_words)        

unique_sorted_words = sorted(set(words))
print("Unique Sorted Words:", unique_sorted_words)


# Section B
#  – Object-Oriented Programming (25 Marks)

'''
3. Class & Inheritance (15 Marks)
- Create a class Employee with attributes: emp_id, name, and salary.
- Create another class Manager (inheriting from Employee) that has an extra attribute 
department.
- Write methods to:
  1. Display employee details.
  2. Display manager details (including department).'''

class Employee:
    def __init__(self,emp_id, name,salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary

    def display_employee(self):
        print(f"Employee ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}")

class Manager(Employee):
    def __init__(self, emp_id, name, salary, department):
        super().__init__(emp_id, name, salary)
        self.department = department

    def display_manager(self):
        print(f"Manager ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}, Department: {self.department}")

emp = Employee(1, "Akshay", 50000)
emp.display_employee()
mgr = Manager(2, "Harshal", 80000, "IT")
mgr.display_manager()


'''4. Encapsulation & Polymorphism (10 Marks)
- Add a method bonus() in both classes:
  - For Employee, return 10% of salary.
  - For Manager, return 20% of salary.
- Demonstrate polymorphism by calling bonus() on both objects.'''


class Employee:
    def __init__(self,emp_id, name,salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary

    def display_employee(self):
        print(f"Employee ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}")

    def bonus(self):
        return self.salary * (10/100)

class Manager(Employee):
    def __init__(self, emp_id, name, salary, department):
        super().__init__(emp_id, name, salary)
        self.department = department

    def display_manager(self):
        print(f"Manager ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}, Department: {self.department}")

    def bonus(self):
        return self.salary * (20/100)

emp = Employee(1, "Akshay", 50000)
emp.display_employee()
mgr = Manager(2, "Harshal", 80000, "IT")
mgr.display_manager()
print("Employee Bonus:", emp.bonus())
print("Manager Bonus:", mgr.bonus())


# Section C
# File Handling & Exception Handling (20 Marks)


'''

5. File Handling (10 Marks)
- Write a Python program that:
  1. Reads a text file data.txt.
  2. Counts the number of lines, words, and characters.
  3. Writes the result into another file summary.txt.

'''

with open('data.txt', 'r') as file:
    content = file.read()
    lines = content.splitlines()
    num_lines = len(lines)
    num_words = len(content.split())
    num_chars = len(content)


with open('summary.txt', 'w') as summary_file:
    summary_file.write(f"Number of lines: {num_lines}\n")
    summary_file.write(f"Number of words: {num_words}\n")
    summary_file.write(f"Number of characters: {num_chars}\n")

'''

6. Exception Handling (10 Marks)
- Write a program that takes a number as input and divides 100 by that number.
- Handle possible exceptions:
  - Division by zero
  - Invalid input (non-numeric values)

'''

n = input("Enter a number to divide 100 by: ")
try:
    n = float(n)
    result = 100 / n
    print("Result:", result)
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")
except ValueError:
    print("Error: Invalid input. Please enter a numeric value.")        


# Section D – Database & Advanced Problems (30 Marks)

'''
7. Python with MySQL (15 Marks)
- Using mysql-connector-python, write a Python program that:
  1. Connects to a MySQL database.
  2. Creates a table students(id, name, marks).
  3. Inserts 3 sample records.
  4. Fetches and displays all records.

'''

from mysql import connector

try:
    conn = connector.connect(
        host='localhost',
        user='root',
        password='akshay',
        database='testdb'
    )
except connector.Error as err:
    print("Error: Could not connect to database:", err)
    exit()

cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INT PRIMARY KEY,
                    name VARCHAR(50),
                    marks INT)''')
cursor.execute("INSERT INTO students (id, name, marks) VALUES (1, 'Alice', 85)")
cursor.execute("INSERT INTO students (id, name, marks) VALUES (2, 'Bob', 90)")
cursor.execute("INSERT INTO students (id, name, marks) VALUES (3, 'Charlie', 95)")
conn.commit()   
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row)
cursor.close()
conn.close()


'''

8. Algorithm Problem (15 Marks)
- Write a Python function longest_substring(s) that returns the longest substring without 
repeating characters.
- Example:
  - Input: "abcabcbb"
  - Output: "abc"
  
'''

def longest_substring(s):
    start = 0
    max_length = 0
    longest_substr = ""
    char_index_map = {}

    for i, char in enumerate(s):
        if char in char_index_map and char_index_map[char] >= start:
            start = char_index_map[char] + 1
        char_index_map[char] = i
        if i - start + 1 > max_length:
            max_length = i - start + 1
            longest_substr = s[start:i+1]

    return longest_substr

print(longest_substring("abcabcbb"))  
print(longest_substring("bbbbb"))    
print(longest_substring("pwwkew"))    
