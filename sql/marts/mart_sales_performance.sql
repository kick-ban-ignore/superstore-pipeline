-- =============================================================================
-- mart_sales_performance.sql
-- Mart Layer: Clean profit per salesperson & category (excluding returns)
-- =============================================================================

CREATE OR REPLACE VIEW mart_sales_performance AS

-- CTE 1: Returned order IDs as a blacklist
WITH returned AS (
    SELECT order_id
    FROM stg_returned_orders
),

-- CTE 2: Orders without returns - this is the clean base
clean_orders AS (
    SELECT o.*
    FROM stg_orders o
    LEFT JOIN returned r ON o.order_id = r.order_id
    WHERE r.order_id IS NULL      -- Anti-join: keep only rows WITHOUT a match
),

-- CTE 3: Join in product info
enriched_orders AS (
    SELECT
        o.order_id,
        o.order_date,
        EXTRACT(YEAR FROM o.order_date)    AS order_year,
        EXTRACT(QUARTER FROM o.order_date) AS order_quarter,
        o.customer_name,
        o.region,
        o.sales,
        o.profit,
        o.quantity,
        o.discount,
        o.shipping_cost,
        p.category,
        p.sub_category,
        p.product_name
    FROM clean_orders o
    LEFT JOIN stg_products p ON o.product_id = p.product_id
),

-- CTE 4: Assign salesperson (person) via region
enriched_with_people AS (
    SELECT
        e.*,
        COALESCE(pe.person, 'Unknown') AS person  -- No NULL if no match
    FROM enriched_orders e
    LEFT JOIN stg_people pe ON e.region = pe.region
)

-- FINAL AGGREGATION: Profit per salesperson & category
SELECT
    person,
    category,
    order_year,
    order_quarter,
    COUNT(DISTINCT order_id)              AS total_orders,
    SUM(quantity)                         AS total_quantity,
    ROUND(SUM(sales), 2)                  AS total_sales,
    ROUND(SUM(profit), 2)                 AS total_profit,
    ROUND(SUM(shipping_cost), 2)          AS total_shipping_cost,
    ROUND(AVG(discount) * 100, 1)         AS avg_discount_pct,
    ROUND(SUM(profit) /
          NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_pct  -- Guard against division by zero!
FROM enriched_with_people
GROUP BY person, category, order_year, order_quarter
ORDER BY order_year DESC, order_quarter DESC, total_profit DESC;