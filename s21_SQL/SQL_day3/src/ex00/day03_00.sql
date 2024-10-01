SELECT
  menu.pizza_name AS pizza_name,
  menu.price AS price,
  pizzeria.name AS pizzeria_name, person_visits.visit_date
FROM person_visits
INNER JOIN menu ON person_visits.pizzeria_id = menu.pizzeria_id
INNER JOIN person ON person_visits.person_id = person.id
INNER JOIN pizzeria ON person_visits.pizzeria_id = pizzeria.id
WHERE person.name =  'Kate' AND (price >= 800 OR price <= 100)
ORDER BY pizza_name, price, pizzeria_name
