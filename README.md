# Amazon E-Commerce Data Analysis & Dashboard 🛒📊

![Dashboard Preview](https://via.placeholder.com/1000x500.png?text=Replace+this+with+a+screenshot+of+your+Dashboard)

## 📌 Project Overview
This project is an end-to-end data analytics solution for an Amazon E-Commerce dataset. It leverages **MySQL** for robust data modeling and advanced querying, alongside **Power BI** for creating comprehensive, interactive dashboards. The goal of this project is to extract actionable business insights regarding revenue growth, customer behavior, product performance, and delivery logistics.

## 🛠️ Tech Stack
- **Database Analytics:** MySQL (CTEs, Window Functions, Joins, Aggregations)
- **Data Visualization & Reporting:** Power BI
- **Documentation & Presentation:** MS Word, MS PowerPoint

## 📂 Project Structure
- **`data_import.sql`**: SQL script to create the database schema (`amazon_ecommerce`), define tables, and load data from CSV files.
- **`objective_tasks.sql`**: Advanced SQL queries answering critical business questions using CTEs, Window Functions, and complex joins.
- **`Amazon_PowerBI_Dashboard.pdf`**: Exported Power BI dashboard showcasing visual analytics and charts.
- **`E-Commerce_Analysis_Presentation.pptx`**: Presentation slides detailing the analysis and business insights.
- **`E-Commerce_Project_Report.docx`**: Detailed project documentation and report.
- **`orders.csv` & `customers.csv`**: The datasets containing order transactions and customer demographics.

## 🗄️ Data Dictionary

### `orders` Table
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **OrderDate** | `DATE` | The date the order was placed. |
| **OrderID** | `INT` | Unique identifier for each order. |
| **DeliveryDate**| `DATE` | The date the order was delivered. |
| **CustomerID** | `INT` | Identifier linking to the customer who placed the order. |
| **Location** | `VARCHAR` | The region/city of the delivery (e.g., Greater Accra, Ashanti). |
| **DeliveryType**| `VARCHAR` | Shipping method (Express, Standard, Shipped from Abroad). |
| **ProductCategory** | `VARCHAR` | Broad category of the product (Electronics, Fashion, etc.). |
| **Product** | `VARCHAR` | Specific product name. |
| **SalePrice** | `DECIMAL` | Total transaction value including unit price and shipping. |
| **Status** | `VARCHAR` | Order status (Delivered, Returned). |
| **Rating** | `INT` | Customer rating from 1 to 5. |

### `customer` Table
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **CustomerID** | `INT` | Unique identifier for each customer. |
| **CustomerAge** | `INT` | Age of the customer. |
| **CustomerGender**| `VARCHAR` | Gender of the customer. |

## 💡 Key SQL Analytical Tasks
The `objective_tasks.sql` file demonstrates advanced SQL problem-solving, including:
- **Composite Customer Scoring:** Identifying top customers based on a weighted score of Revenue (50%), Order Frequency (30%), and Average Order Value (20%).
- **Growth Analysis:** Calculating month-over-month (MoM) revenue growth rates.
- **Trend Analysis:** Computing a rolling 3-month average revenue for each product category.
- **Customer Loyalty:** Determining the average number of days between consecutive orders for returning customers.

## 📊 Power BI Dashboard Insights
The Power BI report provides a deep dive into the business metrics:
- **Sales Analysis:** Tracking **$107.24M** in total revenue across **112.99K** orders, segmented by year and order value tiers (Bronze, Silver, Gold, Platinum).
- **Product Performance:** Analyzing average sale prices and total revenue across categories like Electronics, Phones & Tablets, and Fashion.
- **Logistics & Delivery:** Monitoring average delivery days (9.41 days overall) and comparing shipping fees across different delivery types.

---

## 📈 Business Recommendations 
*(Based on the analysis, here are the strategic recommendations for the business)*

1. **Reduce Return Rates in Electronics:** With over 31K returned products overall, targeting quality control and better product descriptions for high-return categories can immediately impact the bottom line.
2. **Optimize "Shipped from Abroad" Logistics:** The data shows average delivery days for international shipping is significantly higher (15 days). Partnering with regional fulfillment centers for top-selling international items (like Tablets and Cameras) will improve customer satisfaction.
3. **Loyalty Program Expansion:** Since a small percentage of customers drive disproportionately high revenue (identified via the Composite Scoring SQL task), introducing a VIP retention program (e.g., Amazon Prime-style free shipping) for these users will increase Lifetime Value (LTV).

---

## 🚀 How to Run the Project
1. **Database Setup:** 
   - Ensure your MySQL server is running.
   - Place the dataset files (`orders.csv` and `customers.csv`) in your MySQL server's secure uploads directory. *If your path is different, update the path in `data_import.sql`.*
   - Run the `data_import.sql` script to create the tables and import the data.
2. **Data Analysis:**
   - Execute the queries in `objective_tasks.sql` to view the analytical results and business answers.
3. **Dashboard Viewing:**
   - Download and open the `.pbix` file (if provided) in Power BI Desktop, or view the PDF export to see the visualizations.
