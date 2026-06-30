-- =============================================================================
-- stg_orders.sql
-- Staging Layer: Clean & standardize all 4 raw tables
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. stg_orders - Clean the fact table
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW stg_orders AS
SELECT
    order_id,
    order_date::DATE,                    -- Cast text to proper date type
    ship_date::DATE,
    ship_mode,
    customer_id,
    customer_name,
    segment,
    city,
    state,
    country,
    region,
    product_id,
    market,
    ROUND(sales::NUMERIC, 2)         AS sales,
    quantity::INTEGER                AS quantity,
    ROUND(discount::NUMERIC, 2)      AS discount,
    ROUND(profit::NUMERIC, 2)        AS profit,
    ROUND(shipping_cost::NUMERIC, 2) AS shipping_cost,
    order_priority
FROM raw_orders;

-- -----------------------------------------------------------------------------
-- 2. stg_products - Clean the product dimension
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW stg_products AS
SELECT
    product_id,
    TRIM(category)     AS category,      -- Remove surrounding whitespace
    TRIM(sub_category) AS sub_category,
    TRIM(product_name) AS product_name
FROM raw_products;

-- -----------------------------------------------------------------------------
-- 3. stg_people - Clean the salesperson dimension
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW stg_people AS
SELECT
    TRIM(person) AS person,
    TRIM(region) AS region
FROM raw_people;

-- -----------------------------------------------------------------------------
-- 4. stg_returned_orders - Clean the returns
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW stg_returned_orders AS
SELECT DISTINCT         -- DISTINCT! Duplicates in returns tables are common
    order_id,
    market
FROM raw_returned_orders
WHERE returned = 'Yes'; -- Keeps only actual returns