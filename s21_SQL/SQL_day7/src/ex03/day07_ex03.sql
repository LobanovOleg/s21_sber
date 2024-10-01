WITH CTE_order AS (
    SELECT name, COUNT(person_order.id) AS orders
    FROM pizzeria
    JOIN menu ON menu.pizzeria_id = pizzeria.id
    FULL JOIN person_order ON person_order.menu_id = menu.id
    GROUP BY name),
    CTE_visit AS (
    SELECT name, COUNT(person_visits.id) AS visits
    FROM pizzeria
    FULL JOIN person_visits ON person_visits.pizzeria_id = pizzeria.id
    GROUP BY name)
SELECT CTE_order.name, visits + orders AS total_count
FROM CTE_order
JOIN CTE_visit ON CTE_visit.name = CTE_order.name
ORDER BY 2 DESC, 1