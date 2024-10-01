WITH CTE AS (
  SELECT * FROM menu WHERE NOT EXISTS
    (SELECT menu_id FROM person_order WHERE menu_id = menu.id)
)
SELECT
  CTE.pizza_name,
  CTE.price,
  pizzeria.name AS pizzeria_name
FROM CTE INNER JOIN pizzeria ON CTE.pizzeria_id = pizzeria.id
ORDER BY pizza_name, price
