-- ============================================================
-- GREEN MALL: RPC Analytics Functions
-- AIKIVAVIORA Core Analytics MVP
-- ============================================================

-- 1. Выручка по месяцам
CREATE OR REPLACE FUNCTION monthly_revenue()
RETURNS TABLE (
    sale_month TEXT,
    total_revenue NUMERIC
)
LANGUAGE sql
AS $$
    SELECT
        TO_CHAR(s."SalesDate", 'YYYY-MM') AS sale_month,
        ROUND(
            SUM(
                s."Quantity" *
                p."Price" *
                (1 - COALESCE(s."Discount", 0))
            ),
            2
        ) AS total_revenue
    FROM sales s
    JOIN products p
        ON s."ProductID" = p."ProductID"
    WHERE s."SalesDate" IS NOT NULL
    GROUP BY sale_month
    ORDER BY sale_month;
$$;

GRANT EXECUTE ON FUNCTION monthly_revenue() TO anon, authenticated;


-- 2. Топ товаров по выручке
CREATE OR REPLACE FUNCTION top_products(lim INT DEFAULT 10)
RETURNS TABLE (
    product_name TEXT,
    total_revenue NUMERIC
)
LANGUAGE sql
AS $$
    SELECT
        p."ProductName" AS product_name,
        ROUND(
            SUM(
                s."Quantity" *
                p."Price" *
                (1 - COALESCE(s."Discount", 0))
            ),
            2
        ) AS total_revenue
    FROM sales s
    JOIN products p
        ON s."ProductID" = p."ProductID"
    GROUP BY p."ProductName"
    ORDER BY total_revenue DESC
    LIMIT lim;
$$;

GRANT EXECUTE ON FUNCTION top_products(INT) TO anon, authenticated;


-- 3. Выручка по категориям
CREATE OR REPLACE FUNCTION revenue_by_category()
RETURNS TABLE (
    category_name TEXT,
    total_revenue NUMERIC,
    sales_count BIGINT
)
LANGUAGE sql
AS $$
    SELECT
        cat."CategoryName" AS category_name,
        ROUND(
            SUM(
                s."Quantity" *
                p."Price" *
                (1 - COALESCE(s."Discount", 0))
            ),
            2
        ) AS total_revenue,
        COUNT(*) AS sales_count
    FROM sales s
    JOIN products p
        ON s."ProductID" = p."ProductID"
    JOIN categories cat
        ON p."CategoryID" = cat."CategoryID"
    GROUP BY cat."CategoryName"
    ORDER BY total_revenue DESC;
$$;

GRANT EXECUTE ON FUNCTION revenue_by_category() TO anon, authenticated;


-- 4. Топ городов по выручке
CREATE OR REPLACE FUNCTION top_cities(lim INT DEFAULT 10)
RETURNS TABLE (
    city_name TEXT,
    total_revenue NUMERIC,
    sales_count BIGINT
)
LANGUAGE sql
AS $$
    SELECT
        ci."CityName" AS city_name,
        ROUND(
            SUM(
                s."Quantity" *
                p."Price" *
                (1 - COALESCE(s."Discount", 0))
            ),
            2
        ) AS total_revenue,
        COUNT(*) AS sales_count
    FROM sales s
    JOIN customers c
        ON s."CustomerID" = c."CustomerID"
    JOIN cities ci
        ON c."CityID" = ci."CityID"
    JOIN products p
        ON s."ProductID" = p."ProductID"
    GROUP BY ci."CityName"
    ORDER BY total_revenue DESC
    LIMIT lim;
$$;

GRANT EXECUTE ON FUNCTION top_cities(INT) TO anon, authenticated;


-- 5. Топ клиентов по выручке
CREATE OR REPLACE FUNCTION top_customers(lim INT DEFAULT 10)
RETURNS TABLE (
    customer_name TEXT,
    total_revenue NUMERIC
)
LANGUAGE sql
AS $$
    SELECT
        c."FirstName" || ' ' || c."LastName" AS customer_name,
        ROUND(
            SUM(
                s."Quantity" *
                p."Price" *
                (1 - COALESCE(s."Discount", 0))
            ),
            2
        ) AS total_revenue
    FROM sales s
    JOIN customers c
        ON s."CustomerID" = c."CustomerID"
    JOIN products p
        ON s."ProductID" = p."ProductID"
    GROUP BY customer_name
    ORDER BY total_revenue DESC
    LIMIT lim;
$$;

GRANT EXECUTE ON FUNCTION top_customers(INT) TO anon, authenticated;