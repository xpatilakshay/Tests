'''Q1. Data Processing — CSV Sales Report (25 Marks)
Write a Python program `summarize_sales(csv_path: str)` that reads a CSV file with
columns:
date, region, product, units_sold, unit_price
The function should return:
- total_revenue (float) — sum of units_sold * unit_price.
- top_region (str) — region with highest revenue.
- best_selling_product (str) — product with maximum total units sold.
Provide a sample CSV (5 rows) and show the function output.'''

import pandas as pd

def summarize_sales(csv_path: str):
    df = pd.read_csv(csv_path)
    df['revenue'] = df["units_sold"] * df["unit_price"]

    total_revenue = df["revenue"].sum()
    top_region = df.groupby("region")["revenue"].sum().idxmax()
    best_selling_product = df.groupby("product")["units_sold"].sum().idxmax()

    return total_revenue, top_region, best_selling_product


total_revenue, top_region, best_product = summarize_sales("Tests/19 sept Test/data.csv")

print("Total Revenue:", total_revenue)
print("Top Region:", top_region)
print("Best Selling Product:", best_product)

'''Q2. String & Algorithm — Longest Unique Substring (20 Marks)
Write a function `longest_unique_substring(s: str) -> str` that returns the longest substring
without repeating characters.
Show output for test cases:
- "abcabcbb" -> "abc"
- "bbbbb" -> "b"
- "pwwkew" -> "wke"
Also provide time and space complexity analysis'''

def longest_unique_substring(s: str) -> str:
    start = 0
    seen = {}
    max_len = 0
    max_substr = ""

    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1
        seen[ch] = i
        if i - start + 1 > max_len:
            max_len = i - start + 1
            max_substr = s[start:i+1]
    return max_substr


print(longest_unique_substring("abcabcbb"))  
print(longest_unique_substring("bbbbb"))     
print(longest_unique_substring("pwwkew"))   




'''Q3. Object-Oriented Design — LRU Cache (20 Marks)
Implement a class `LRUCache` with methods get(key) and put(key, value) and a fixed
capacity.
Do not use functools.lru_cache or OrderedDict.
Write short test code to show cache eviction order.'''

class Node:
    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

        # Dummy head/tail
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _add(self, node):
        prev, nxt = self.tail.prev, self.tail
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add(node)

        if len(self.cache) > self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]



cache = LRUCache(2)
cache.put(1, 10)
cache.put(2, 20)
print(cache.get(1))  
cache.put(3, 30)     
print(cache.get(2))  
cache.put(4, 40)     
print(cache.get(1))  
print(cache.get(3))  
print(cache.get(4))  



'''Q4. Debugging — Fix the Code (15 Marks)
The following function is intended to flatten nested lists. Fix the bug and explain your
changes:
def flatten(arr):
 result = []
 for x in arr:
 if isinstance(x, list):
 result.extend(flatten(x))
 else:
 result.append(x)
 return result
print(flatten([1, [2, [3, 4]], 5])) # Expected [1, 2, 3, 4, 5]'''


def flatten(arr):
    result = []
    for x in arr:
        if isinstance(x, list):
            result.extend(flatten(x))
        else:
            result.append(x)
    return result

print(flatten([1, [2, [3, 4]], 5])) # Expected [1, 2, 3, 4, 5]

'''

Q5. File Handling & JSON (20 Marks)
Write a Python program that reads a JSON file `students.json` containing a list of students
with fields:
name, marks (list of integers)
The program should:
- Compute average marks of each student.
- Save the result in a new JSON file `student_report.json` with fields: name, average.
- Show a sample input file and the corresponding output file.

'''

import json


def process_students(input_file:str,output_file:str):
    with open(input_file,"r") as f:
        students = json.load(f)

    report = []

    for s in students:
        avg = sum(s["marks"])/len(s["marks"]) if s["marks"] else 0
        report.append({"name":s["name"],"average":avg})

    with open(output_file,"w") as f:
        json.dump(report,f,indent=4)
        print(f"data stored in \"{output_file}\" succesfully ")

process_students("Tests/19 sept Test/student.json", "student_report.json")
