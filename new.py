products = [
    {"name": "Laptop", "price": 80000},
    {"name": "Phone", "price": 50000},
    {"name": "Tablet", "price": 30000},
    {"name": "Monitor", "price": 25000}
]
highest = max(products,key =lambda price:price["price"])
lowest = min(products,key=lambda price:price["price"])

print(f"The most expesnive device is {highest["name"]} at {highest["price"]}")

print(f"The least expensive is {lowest["name"]} at {lowest["price"]}")



