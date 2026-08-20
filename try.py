employees = [
    {"name": "Alice", "department": "Engineering", "salary": 80000},
    {"name": "Bob", "department": "Sales", "salary": 60000},
    {"name": "Charlie", "department": "Engineering", "salary": 90000},
    {"name": "David", "department": "HR", "salary": 55000},
    {"name": "Eve", "department": "Sales", "salary": 70000},
    {"name": "Frank", "department": "Engineering", "salary": 75000}
]
highest = []

for employee in employees:
    salary = employee["salary"]
    name = employee["name"]
    if salary > 70000:
        highest.append(name)
print(highest)





       