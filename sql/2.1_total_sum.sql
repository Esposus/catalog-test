SELECT c.name AS client_name, SUM(oi.quantity * p.price) AS total_sum
FROM clients c
JOIN orders o ON c.id = o.client_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY c.id, c.name;
