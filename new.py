students = [
    {"name": "Alice", "score": 82},
    {"name": "Bob", "score": 48},
    {"name": "Charlie", "score": 91},
    {"name": "David", "score": 76}
]
above_90 = any(student["score"] >90 for student in students)
above_50 = all(student["score"] >50 for student in students)
print(above_50)
print(above_90)