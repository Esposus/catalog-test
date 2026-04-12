CREATE OR REPLACE VIEW top5_products_last_month AS WITH RECURSIVE category_root AS (
    SELECT id, id AS root_id
    FROM categories
    WHERE parent_id IS NULL
)
