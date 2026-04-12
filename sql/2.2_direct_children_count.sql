SELECT cat.name AS category_name, COUNT (child.id) AS direct_children_count
FROM categories cat
LEFT JOIN categories child ON cat.id = child.parent_id
GROUP BY cat.id, cat.name
ORDER BY direct_children_id DESC;
