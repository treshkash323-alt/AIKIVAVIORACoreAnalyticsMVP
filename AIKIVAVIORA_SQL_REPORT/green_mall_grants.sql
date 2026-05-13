-- ============================================================
-- GREEN MALL: Grants and RLS Policies
-- AIKIVAVIORA Core Analytics MVP
-- ============================================================

ALTER TABLE countries  ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE cities     ENABLE ROW LEVEL SECURITY;
ALTER TABLE employees  ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers  ENABLE ROW LEVEL SECURITY;
ALTER TABLE products   ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales      ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read countries"
ON countries FOR SELECT TO anon, authenticated
USING (true);

CREATE POLICY "Allow public read categories"
ON categories FOR SELECT TO anon, authenticated
USING (true);

CREATE POLICY "Allow public read cities"
ON cities FOR SELECT TO anon, authenticated
USING (true);

CREATE POLICY "Allow public read employees"
ON employees FOR SELECT TO anon, authenticated
USING (true);

CREATE POLICY "Allow public read customers"
ON customers FOR SELECT TO anon, authenticated
USING (true);

CREATE POLICY "Allow public read products"
ON products FOR SELECT TO anon, authenticated
USING (true);

CREATE POLICY "Allow public read sales"
ON sales FOR SELECT TO anon, authenticated
USING (true);

GRANT SELECT ON countries, categories, cities, employees, customers, products, sales
TO anon, authenticated;