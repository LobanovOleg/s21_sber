CREATE INDEX idx_1 ON pizzeria(rating);
SET enable_seqscan TO OFF;
EXPLAIN ANALYSE
SELECT 
    menu.pizza_name AS pizza_name,
    MAX(rating) OVER (PARTITION BY rating ORDER BY rating ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
FROM menu
INNER JOIN pizzeria ON menu.pizzeria_id = pizzeria.id
ORDER BY 1, 2;

DROP INDEX idx_1;
EXPLAIN ANALYSE
SELECT
    menu.pizza_name AS pizza_name,
    MAX(rating) OVER (PARTITION BY rating ORDER BY rating ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
FROM menu
INNER JOIN pizzeria ON menu.pizzeria_id = pizzeria.id
ORDER BY 1, 2