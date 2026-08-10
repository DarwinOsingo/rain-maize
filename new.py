products = ["Laptop", "Phone", "Tablet", "Monitor"]
prices = [80000, 50000, 30000, 25000]

elecs = dict(zip(products,prices))
for products,prices in elecs.items():
    print(f"{products:<10}:{prices}")
