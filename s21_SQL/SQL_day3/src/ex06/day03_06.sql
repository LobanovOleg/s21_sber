SELECT
  q1.pizza_name, p1.name AS pizzeria_name_1, p2.name AS pizzeria_name_2, q1.price
FROM menu AS q1
INNER JOIN menu AS q2 ON q1.price = q2.price
INNER JOIN pizzeria AS p1 ON q1.pizzeria_id = p1.id
INNER JOIN pizzeria AS p2 ON q2.pizzeria_id = p2.id
WHERE q1.id > q2.id AND q1.pizza_name = q2.pizza_name
ORDER BY pizza_name
