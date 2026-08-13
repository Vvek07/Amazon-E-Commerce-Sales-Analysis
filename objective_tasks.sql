-- ============================================================
-- Task 14
-- Identify the top 5 most valuable customers using a composite
-- score: Revenue (50%), Order Frequency (30%), AOV (20%)
-- ============================================================

WITH customer_metrics AS (
    SELECT
        CustomerID,
        SUM(SalePrice) AS Total_Revenue,
        COUNT(OrderID) AS Order_Frequency,
        AVG(SalePrice) AS Avg_Order_Value
    FROM orders
    GROUP BY CustomerID
),
normalized_metrics AS (
    SELECT
        *,
        Total_Revenue / MAX(Total_Revenue) OVER () AS Revenue_Score,
        Order_Frequency / MAX(Order_Frequency) OVER () AS Frequency_Score,
        Avg_Order_Value / MAX(Avg_Order_Value) OVER () AS AOV_Score
    FROM customer_metrics
)
SELECT
    CustomerID,
    Total_Revenue,
    Order_Frequency,
    ROUND(Avg_Order_Value, 2) AS Avg_Order_Value,
    ROUND(
        (Revenue_Score * 0.50) +
        (Frequency_Score * 0.30) +
        (AOV_Score * 0.20),
        4
    ) AS Composite_Score
FROM normalized_metrics
ORDER BY Composite_Score DESC
LIMIT 5;


-- ============================================================
-- Task 15
-- Calculate the month-over-month growth rate in total revenue
-- across the entire dataset
-- ============================================================

WITH month_group AS (
    SELECT
        LEFT(OrderDate, 7) AS Month,
        SUM(SalePrice) AS Total_Revenue
    FROM orders
    GROUP BY LEFT(OrderDate, 7)
),
prev_data AS (
    SELECT
        Month,
        Total_Revenue,
        LAG(Total_Revenue) OVER (ORDER BY Month) AS Previous_Month_Revenue
    FROM month_group
)
SELECT
    Month,
    Total_Revenue,
    Previous_Month_Revenue,
    ROUND(
        ((Total_Revenue - Previous_Month_Revenue)
        / NULLIF(Previous_Month_Revenue, 0)) * 100,
        2
    ) AS Growth_Rate
FROM prev_data
ORDER BY Month;


-- ============================================================
-- Task 16
-- Calculate the rolling 3-month average revenue
-- for each product category
-- ============================================================

WITH category_data AS (
    SELECT
        ProductCategory,
        DATE_FORMAT(OrderDate, '%Y-%m') AS Month,
        SUM(SalePrice) AS Total_Revenue
    FROM orders
    GROUP BY
        ProductCategory,
        DATE_FORMAT(OrderDate, '%Y-%m')
)
SELECT
    ProductCategory,
    Month,
    Total_Revenue,
    ROUND(
        AVG(Total_Revenue) OVER (
            PARTITION BY ProductCategory
            ORDER BY Month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS Rolling_Average_3_Month
FROM category_data
ORDER BY ProductCategory, Month;


-- ============================================================
-- Task 17
-- Apply a 15% discount on SalePrice for customers
-- who have made at least 10 orders
-- ============================================================

UPDATE orders
SET SalePrice = SalePrice * 0.85
WHERE CustomerID IN (
    SELECT CustomerID
    FROM orders
    GROUP BY CustomerID
    HAVING COUNT(*) >= 10
);


-- ============================================================
-- Task 18
-- Calculate the average number of days between consecutive
-- orders for customers who have placed at least five orders
-- ============================================================

WITH qualified_customers AS (
    SELECT
        CustomerID
    FROM orders
    GROUP BY CustomerID
    HAVING COUNT(*) >= 5
),
order_intervals AS (
    SELECT
        CustomerID,
        OrderDate,
        DATEDIFF(
            OrderDate,
            LAG(OrderDate) OVER (
                PARTITION BY CustomerID
                ORDER BY OrderDate
            )
        ) AS Days_Between_Orders
    FROM orders
    WHERE CustomerID IN (
        SELECT CustomerID
        FROM qualified_customers
    )
)
SELECT
    ROUND(AVG(Days_Between_Orders), 2)
        AS Average_Days_Between_Orders
FROM order_intervals
WHERE Days_Between_Orders IS NOT NULL;


-- ============================================================
-- Task 19
-- Identify customers who have generated revenue that is
-- more than 30% higher than the average revenue per customer
-- ============================================================

WITH Customer_data AS (
    SELECT
        CustomerID,
        SUM(SalePrice) AS Total_Revenue
    FROM orders
    GROUP BY CustomerID
),
Average_data AS (
    SELECT
        AVG(Total_Revenue) AS Average_Revenue
    FROM Customer_data
)
SELECT
    c.CustomerID,
    c.Total_Revenue,
    ROUND(a.Average_Revenue, 2) AS Average_Revenue,
    ROUND(
        ((c.Total_Revenue - a.Average_Revenue)
        / a.Average_Revenue) * 100,
        2
    ) AS Percentage_Above_Average
FROM Customer_data c
CROSS JOIN Average_data a
WHERE c.Total_Revenue > a.Average_Revenue * 1.30
ORDER BY c.Total_Revenue DESC;


-- ============================================================
-- Task 20
-- Determine the top 3 product categories that have shown
-- the highest increase in sales over the past year compared
-- to the previous year
-- ============================================================

WITH yearly_sales AS (
    SELECT
        ProductCategory,
        YEAR(OrderDate) AS Order_Year,
        SUM(SalePrice) AS Total_Sales
    FROM orders
    GROUP BY
        ProductCategory,
        YEAR(OrderDate)
),
latest_years AS (
    SELECT
        MAX(Order_Year) AS Latest_Year
    FROM yearly_sales
),
sales_comparison AS (
    SELECT
        ProductCategory,
        MAX(
            CASE
                WHEN Order_Year =
                    (SELECT Latest_Year FROM latest_years)
                THEN Total_Sales
            END
        ) AS Current_Year_Sales,
        MAX(
            CASE
                WHEN Order_Year =
                    (SELECT Latest_Year FROM latest_years) - 1
                THEN Total_Sales
            END
        ) AS Previous_Year_Sales
    FROM yearly_sales
    GROUP BY ProductCategory
)
SELECT
    ProductCategory,
    Current_Year_Sales,
    Previous_Year_Sales,
    Current_Year_Sales - Previous_Year_Sales AS Sales_Increase,
    ROUND(
        ((Current_Year_Sales - Previous_Year_Sales)
        / NULLIF(Previous_Year_Sales, 0)) * 100,
        2
    ) AS Growth_Rate
FROM sales_comparison
WHERE Previous_Year_Sales IS NOT NULL
  AND Current_Year_Sales IS NOT NULL
ORDER BY Sales_Increase DESC
LIMIT 3;