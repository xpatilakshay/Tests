
# Section A: Core Python & Logic (20 Marks)
# 1. Matrix Rotation (10 Marks)
# Write a program to rotate a 2D matrix by 90 degrees without using external libraries.
# Example:
# Input:
# [[1,2,3],
#  [4,5,6],
#  [7,8,9]]
# Output:
# [[7,4,1],
#  [8,5,2],
#  [9,6,3]]


def rotation(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i,n):
            matrix[i][j],matrix[j][i] = matrix[j][i],matrix[i][j] 
    for j in range(n):
          start = 0
          end = n -1
          while start<end:
            matrix[j][start],matrix[j][end] = matrix[j][end],matrix[j][start]
            start+=1
            end-=1
    return matrix

matrix = [[1,2,3],
         [4,5,6],
         [7,8,9]]

print(rotation(matrix))


# 2. Generator Function (10 Marks)
# Write a generator function prime_generator(n) that yields all prime numbers up to n.
# Use it to print primes up to 50


def prime_generator(n):
    is_prime = False
    for num in range(2,n+1):
            is_prime = True
            for i in range(2,int(num**0.5)+1):
                if num%i==0:
                    is_prime=  False
                    break
            if is_prime:
                yield num

result = prime_generator(50)
for num in result:
    print(num)


# 3. Decorator – Execution Time (10 Marks)
# Write a decorator @timing that calculates how long a function takes to execute.
# Test it with a function that sums numbers from 1 to 1,000,000.

import time

def timing(func):
    def wrapper():
        start_time = time.time()
        result = func()
        time_taken = time.time()-start_time
        print("Time Taken to execute functionis : ",time_taken)
        return result
    return wrapper

@timing
def summer():
    sum = 0
    for i in range(1,1000000+1):
        sum = sum+i
    return sum

print("Sum of numbers from 1 to 1000000 is : ",summer())    


# 4. Text File Word Analyzer (10 Marks)
# Given a text file data.txt, write a program to:
# - Count total words
# - Find the 5 most frequent words
# - Ignore case sensitivity

from collections import Counter

def analyze_text(filename):
    with open(filename, "r") as file:
        text = file.read().lower()  
    
    words = text.split()
    total_words = len(words)
    freq = Counter(words).most_common(5)
    
    print(f"Total Words: {total_words}")
    print("Top 5 Frequent Words:")
    for word, count in freq:
        print(word, "-", count)

analyze_text("data.txt")

# 5. OOP + Inheritance (10 Marks)
# Design classes for a Vehicle System:
# - Base class: Vehicle (brand, model, price)
# - Subclass: Car (seating_capacity)
# - Subclass: Bike (engine_cc)
# Create objects and print their details using __str__.

class Vehicle:
    def __init__(self,brand,model,price):
        self.brand = brand
        self.model = model
        self.price = price

    def __str__(self):
        return f"Brand : {self.brand}, Model : {self.model} , Price : {self.price}"
        

class Car(Vehicle):
    def __init__(self,brand,model,price,seating_capacity):
        super().__init__(brand,model,price)
        self.seating_capacity = seating_capacity

    def __str__(self):
        return f"{super().__str__()}, Seating Capacity : {self.seating_capacity} "

class Bike(Vehicle):
    def __init__(self,brand,model,price,engine_cc):
        super().__init__(brand,model,price)
        self.engine_cc = engine_cc

    def __str__(self):
        return f"{super().__str__()}, Engine CC : {self.engine_cc}"

car1 = Car("Toyota", "Camry", 30000, 5)
bike1 = Bike("Honda", "CBR500R", 7000, 500)


print(car1)
print(bike1)


# 6. API + Data Processing (10 Marks)
# Fetch weather data from API:
# https://api.open-meteo.com/v1/forecast?
# latitude=20&longitude=77&hourly=temperature_2m
# - Print the highest temperature of the day
# - Print the average temperature


import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=20&longitude=77&hourly=temperature_2m"

response = requests.get(url)
data = response.json()

temperatures = data['hourly']['temperature_2m']

highest_temp = max(temperatures)
average_temp = sum(temperatures) / len(temperatures)

print(f"Highest temperature of the day: {highest_temp}°C")
print(f"Average temperature of the day: {average_temp:.2f}°C")


# Section C: Real-World Mini Projects (40 Marks)
# 7. Mini Project – Student Result System (40 Marks)
# Build a Python program that manages student exam results.
# Requirements:
# - Store data in SQLite (students(id, name, subject, marks))
# - Insert at least 10 records across multiple subjects
# - Write functions to:
#  - Add a new student record
#  - Fetch all records of a student by id
#  - Calculate total and average marks of a student
#  - Display top 3 students overall based on average marks
# Extra Credit:
# - Export top 3 students’ data to a top_students.json file

import sqlite3
import json

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER,
    name TEXT,
    subject TEXT,
    marks INTEGER
)
""")

sample_data = [
    (1, "Alice", "Math", 85),
    (1, "Alice", "Science", 90),
    (1, "Alice", "English", 78),
    (2, "Bob", "Math", 92),
    (2, "Bob", "Science", 88),
    (2, "Bob", "English", 84),
    (3, "Charlie", "Math", 70),
    (3, "Charlie", "Science", 75),
    (3, "Charlie", "English", 80),
    (4, "David", "Math", 95),
    (4, "David", "Science", 90),
    (4, "David", "English", 85)
]

cursor.execute("SELECT COUNT(*) FROM students")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", sample_data)
    conn.commit()

def add_student_record(student_id, name, subject, marks):
    cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (student_id, name, subject, marks))
    conn.commit()
    print(f"Record added for {name} in {subject}.")

def fetch_student_records(student_id):
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    records = cursor.fetchall()
    if records:
        for r in records:
            print(f"ID: {r[0]}, Name: {r[1]}, Subject: {r[2]}, Marks: {r[3]}")
    else:
        print("No records found.")

def calculate_total_average(student_id):
    cursor.execute("SELECT marks FROM students WHERE id=?", (student_id,))
    marks = [r[0] for r in cursor.fetchall()]
    if marks:
        total = sum(marks)
        average = total / len(marks)
        print(f"Total Marks: {total}, Average Marks: {average:.2f}")
    else:
        print("No marks found for this student.")

def top_3_students():
    cursor.execute("""
    SELECT id, name, AVG(marks) as avg_marks
    FROM students
    GROUP BY id, name
    ORDER BY avg_marks DESC
    LIMIT 3
    """)
    top_students = cursor.fetchall()
    print("Top 3 Students:")
    for i, student in enumerate(top_students, start=1):
        print(f"{i}. {student[1]} (ID: {student[0]}), Average Marks: {student[2]:.2f}")
    return top_students

def export_top_students_json():
    top_students_data = top_3_students()
    students_list = [
        {"id": s[0], "name": s[1], "average_marks": s[2]}
        for s in top_students_data
    ]
    with open("top_students.json", "w") as f:
        json.dump(students_list, f, indent=4)
    print("Top 3 students exported to top_students.json")

add_student_record(5, "Eva", "Math", 88)
add_student_record(5, "Eva", "Science", 92)

print("\nRecords for student ID 1:")
fetch_student_records(1)

print("\nTotal and average for student ID 2:")
calculate_total_average(2)

print("\nTop 3 students overall:")
top_3_students()

export_top_students_json()

conn.close()