import csv
import random
from datetime import datetime, timedelta

# Configuration
NUM_CUSTOMERS = 1000
NUM_ORDERS = 5000

categories = {
    "Electronics": ["Digital Cameras", "Smartwatches", "Home Theatre"],
    "Phones and Tablet": ["Mobile phones", "Tablets"],
    "Fashion": ["Clothing", "Shoes", "Accessories"],
    "Health and beauty": ["Personal Care", "Makeup"],
    "Home and Office": ["Furniture", "Stationery"]
}

products = {
    "Digital Cameras": ["Canon EOS 600D 18MP CMOS DSLR", "Nikon D3500", "Sony Alpha a6000"],
    "Smartwatches": ["Apple Watch Series 6", "Samsung Galaxy Watch 3"],
    "Home Theatre": ["Sony 5.1 Home Theatre", "LG Soundbar"],
    "Mobile phones": ["Samsung Galaxy A02", "Infinix Smart HD X612", "iPhone 12"],
    "Tablets": ["Amazon Fire HD 8 Kids Tablet", "iPad Air 4th Gen"],
    "Clothing": ["100% Cotton 4 Piece T-Shirts", "Men's Denim Jacket"],
    "Shoes": ["Nike Air Max", "Adidas Ultraboost"],
    "Accessories": ["Leather Wallet", "Polarized Sunglasses"],
    "Personal Care": ["Aichun Beauty Essential Oil", "Avon Soft Musk Spray"],
    "Makeup": ["MAC Lipstick", "Maybelline Foundation"],
    "Furniture": ["8 Cubes Plastic Wardrobe", "Ergonomic Office Chair"],
    "Stationery": ["Parker Pen", "Moleskine Notebook"]
}

locations = ["Greater Accra", "Ashanti", "Western", "Weija", "Volta", "Upper East", "Oti"]
zones = ["North", "South", "East", "West", "Central"]
delivery_types = ["Standard Delivery", "Express", "Shipped from Abroad"]
statuses = ["Delivered", "Returned", "Cancelled"]
reasons = ["Defective", "Arrived Late", "Changed Mind", "Not as expected"]

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

start_date = datetime.strptime('2015-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2020-12-31', '%Y-%m-%d')

# Generate Customers
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "CustomerID": i,
        "CustomerAge": random.randint(18, 70),
        "CustomerGender": random.choice(["Male", "Female", "Other"])
    })

# Write customers.csv
with open("customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["CustomerID", "CustomerAge", "CustomerGender"])
    writer.writeheader()
    writer.writerows(customers)

# Generate Orders
orders = []
for i in range(1, NUM_ORDERS + 1):
    customer = random.choice(customers)
    order_date = random_date(start_date, end_date)
    delivery_days = random.randint(2, 20)
    delivery_date = order_date + timedelta(days=delivery_days)
    
    cat = random.choice(list(categories.keys()))
    sub_cat = random.choice(categories[cat])
    prod = random.choice(products[sub_cat])
    
    unit_price = round(random.uniform(10.0, 1500.0), 2)
    qty = random.randint(1, 5)
    shipping = round(random.uniform(5.0, 50.0), 2)
    sale_price = (unit_price * qty) + shipping
    
    status = random.choices(statuses, weights=[70, 25, 5])[0]
    rating = random.choices([1, 2, 3, 4, 5], weights=[20, 20, 30, 20, 10])[0] if status == "Delivered" else random.choice([1, 2])
    reason = random.choice(reasons) if status != "Delivered" else ""
    
    orders.append({
        "OrderDate": order_date.strftime('%Y-%m-%d'),
        "OrderID": i,
        "DeliveryDate": delivery_date.strftime('%Y-%m-%d'),
        "CustomerID": customer["CustomerID"],
        "Location": random.choice(locations),
        "Zone": random.choice(zones),
        "DeliveryType": random.choice(delivery_types),
        "ProductCategory": cat,
        "SubCategory": sub_cat,
        "Product": prod,
        "UnitPrice": unit_price,
        "ShippingFee": shipping,
        "OrderQuantity": qty,
        "SalePrice": round(sale_price, 2),
        "Status": status,
        "Rating": rating,
        "Reason": reason,
        "Customer_age": customer["CustomerAge"],
        "Delivery_days": delivery_days
    })

# Write orders.csv
fieldnames = ["OrderDate", "OrderID", "DeliveryDate", "CustomerID", "Location", "Zone", "DeliveryType", 
              "ProductCategory", "SubCategory", "Product", "UnitPrice", "ShippingFee", "OrderQuantity", 
              "SalePrice", "Status", "Rating", "Reason", "Customer_age", "Delivery_days"]

with open("orders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)

print("Generated customers.csv and orders.csv successfully.")
