import csv
import random
from datetime import datetime, timedelta

NUM_ORDERS = 112990
NUM_CUSTOMERS = 102000

print("Generating perfectly synced dataset. This may take a moment...")

categories = {
    "Electronics": ["Digital Cameras", "Smartwatches", "Home Theatre"],
    "Phones and Tablet": ["Mobile phones", "Tablets"],
    "Fashion": ["Clothing", "Shoes", "Accessories"],
    "Health and beauty": ["Personal Care", "Makeup"],
    "Home and Office": ["Furniture", "Stationery"]
}

# Exactly 44 products
products = [
    # Electronics (10)
    ("Canon EOS 600D 18MP", "Electronics", "Digital Cameras", 500.0),
    ("Nikon D3500", "Electronics", "Digital Cameras", 450.0),
    ("Sony Alpha a6000", "Electronics", "Digital Cameras", 600.0),
    ("Apple Watch Series 6", "Electronics", "Smartwatches", 400.0),
    ("Samsung Galaxy Watch 3", "Electronics", "Smartwatches", 350.0),
    ("Fitbit Versa 3", "Electronics", "Smartwatches", 200.0),
    ("Sony 5.1 Home Theatre", "Electronics", "Home Theatre", 800.0),
    ("LG Soundbar", "Electronics", "Home Theatre", 300.0),
    ("Bose QuietComfort", "Electronics", "Home Theatre", 350.0),
    ("JBL Flip 5", "Electronics", "Home Theatre", 100.0),
    # Phones (8)
    ("Samsung Galaxy A02", "Phones and Tablet", "Mobile phones", 150.0),
    ("Infinix Smart HD X612", "Phones and Tablet", "Mobile phones", 100.0),
    ("iPhone 12", "Phones and Tablet", "Mobile phones", 800.0),
    ("OnePlus 9", "Phones and Tablet", "Mobile phones", 700.0),
    ("Google Pixel 5", "Phones and Tablet", "Mobile phones", 600.0),
    ("Amazon Fire HD 8 Kids", "Phones and Tablet", "Tablets", 140.0),
    ("iPad Air 4th Gen", "Phones and Tablet", "Tablets", 600.0),
    ("Samsung Galaxy Tab S7", "Phones and Tablet", "Tablets", 650.0),
    # Fashion (10)
    ("100% Cotton 4 Piece T-Shirts", "Fashion", "Clothing", 40.0),
    ("Men's Denim Jacket", "Fashion", "Clothing", 60.0),
    ("Women's Summer Dress", "Fashion", "Clothing", 50.0),
    ("Nike Air Max", "Fashion", "Shoes", 120.0),
    ("Adidas Ultraboost", "Fashion", "Shoes", 180.0),
    ("Puma Running Shoes", "Fashion", "Shoes", 80.0),
    ("Leather Wallet", "Fashion", "Accessories", 30.0),
    ("Polarized Sunglasses", "Fashion", "Accessories", 25.0),
    ("Silver Necklace", "Fashion", "Accessories", 70.0),
    ("Canvas Backpack", "Fashion", "Accessories", 45.0),
    # Health (8)
    ("Aichun Beauty Essential Oil", "Health and beauty", "Personal Care", 15.0),
    ("Avon Soft Musk Spray", "Health and beauty", "Personal Care", 20.0),
    ("Dove Body Wash", "Health and beauty", "Personal Care", 10.0),
    ("Nivea Men Lotion", "Health and beauty", "Personal Care", 12.0),
    ("MAC Lipstick", "Health and beauty", "Makeup", 25.0),
    ("Maybelline Foundation", "Health and beauty", "Makeup", 15.0),
    ("L'Oreal Mascara", "Health and beauty", "Makeup", 18.0),
    ("Urban Decay Palette", "Health and beauty", "Makeup", 50.0),
    # Home (8)
    ("8 Cubes Plastic Wardrobe", "Home and Office", "Furniture", 80.0),
    ("Ergonomic Office Chair", "Home and Office", "Furniture", 150.0),
    ("Wooden Desk", "Home and Office", "Furniture", 200.0),
    ("Bookshelf", "Home and Office", "Furniture", 100.0),
    ("Parker Pen", "Home and Office", "Stationery", 25.0),
    ("Moleskine Notebook", "Home and Office", "Stationery", 20.0),
    ("Desk Organizer", "Home and Office", "Stationery", 15.0),
    ("Whiteboard", "Home and Office", "Stationery", 40.0)
]

locations = ["Greater Accra", "Ashanti", "Western", "Weija", "Volta", "Upper East", "Oti"]
zones = ["North", "South", "East", "West", "Central"]
delivery_types = ["Standard Delivery", "Express", "Shipped from Abroad"]

# 1. Generate Customers
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "CustomerID": i,
        "CustomerAge": random.randint(18, 70),
        "CustomerGender": random.choices(["Male", "Female", "Other"], weights=[45, 50, 5])[0]
    })

with open("customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["CustomerID", "CustomerAge", "CustomerGender"])
    writer.writeheader()
    writer.writerows(customers)

# 2. Generate Orders
start_date = datetime(2015, 1, 1)
end_date = datetime(2020, 12, 31)
date_range = (end_date - start_date).days

orders = []
total_revenue = 0
total_qty = 0

TARGET_REVENUE = 107240000
TARGET_QTY = 603000

for i in range(1, NUM_ORDERS + 1):
    # Base randomized data
    order_date = start_date + timedelta(days=random.randint(0, date_range))
    delivery_days = int(random.gauss(9.53, 2))
    delivery_days = max(1, min(delivery_days, 30))
    delivery_date = order_date + timedelta(days=delivery_days)
    
    prod_name, cat, subcat, base_price = random.choice(products)
    
    # Target 31K returns (~27.4%)
    is_returned = random.random() < (31000 / 112990)
    status = "Returned" if is_returned else "Delivered"
    
    # Ratings targeting 2.73 average
    if is_returned:
        rating = random.choices([1, 2], weights=[70, 30])[0]
    else:
        rating = random.choices([3, 4, 5], weights=[40, 40, 20])[0]
    
    reason = random.choice(["Defective", "Late Delivery", "Changed Mind"]) if is_returned else ""
    
    # We need to scale pricing to hit exactly $107.24M revenue and 603K quantity
    # Average quantity needed = 603000 / 112990 = 5.33
    qty = max(1, int(random.gauss(5.33, 2)))
    
    # Average order value needed = 949
    # Current base_price * qty might be off. We will just use a scalar.
    unit_price = base_price * 1.5 # Boost base price to hit target
    shipping = random.uniform(5, 20)
    sale_price = (unit_price * qty) + shipping
    
    cust = random.choice(customers)
    
    orders.append({
        "OrderDate": order_date.strftime('%Y-%m-%d'),
        "OrderID": i,
        "DeliveryDate": delivery_date.strftime('%Y-%m-%d'),
        "CustomerID": cust["CustomerID"],
        "Location": random.choice(locations),
        "Zone": random.choice(zones),
        "DeliveryType": random.choice(delivery_types),
        "ProductCategory": cat,
        "SubCategory": subcat,
        "Product": prod_name,
        "UnitPrice": round(unit_price, 2),
        "ShippingFee": round(shipping, 2),
        "OrderQuantity": qty,
        "SalePrice": sale_price, # We'll round this after adjustment
        "Status": status,
        "Rating": rating,
        "Reason": reason,
        "Customer_age": cust["CustomerAge"],
        "Delivery_days": delivery_days
    })
    
    total_revenue += sale_price
    total_qty += qty

# 3. Adjustment Pass
# To hit exactly 107.24M revenue, we multiply all sale prices by the ratio
revenue_ratio = TARGET_REVENUE / total_revenue
qty_diff = TARGET_QTY - total_qty

for order in orders:
    order["SalePrice"] = round(order["SalePrice"] * revenue_ratio, 2)
    # Adjust unit price to make math look correct (SalePrice - Shipping) / Qty
    order["UnitPrice"] = round((order["SalePrice"] - order["ShippingFee"]) / order["OrderQuantity"], 2)

# Adjust quantities if we are slightly off 603000
while qty_diff != 0:
    idx = random.randint(0, len(orders)-1)
    if qty_diff > 0:
        orders[idx]["OrderQuantity"] += 1
        qty_diff -= 1
    elif qty_diff < 0 and orders[idx]["OrderQuantity"] > 1:
        orders[idx]["OrderQuantity"] -= 1
        qty_diff += 1
        
    orders[idx]["UnitPrice"] = round((orders[idx]["SalePrice"] - orders[idx]["ShippingFee"]) / orders[idx]["OrderQuantity"], 2)

fieldnames = ["OrderDate", "OrderID", "DeliveryDate", "CustomerID", "Location", "Zone", "DeliveryType", 
              "ProductCategory", "SubCategory", "Product", "UnitPrice", "ShippingFee", "OrderQuantity", 
              "SalePrice", "Status", "Rating", "Reason", "Customer_age", "Delivery_days"]

with open("orders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)

print("Generated exactly 112,990 orders.")
print(f"Total Revenue Target: $107,240,000")
print(f"Total Quantity Target: 603,000")
