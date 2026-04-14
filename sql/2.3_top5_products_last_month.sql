CREATE OR REPLACE VIEW top5_products_last_month AS
WITH RECURSIVE category_root AS (
    SELECT id, id AS root_id
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, cr.root_id
    FROM categories c
    JOIN category_root cr ON c.parent_id = cr.id
)
SELECT p.name AS product_name, root_cat.name AS level1_category, SUM(oi.quantity) AS total_sold
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN category_root cr ON p.category_id = cr.id
JOIN categories root_cat ON cr.root_id = root_cat.id
WHERE o.created_at >= date_trunc('month', CURRENT_DATE - INTERVAL '1 month') AND o.created_at <  date_trunc('month', CURRENT_DATE)
GROUP BY p.name, root_cat.name, p.id, root_cat.id
ORDER BY total_sold DESC
LIMIT 5;
