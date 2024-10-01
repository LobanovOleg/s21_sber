SELECT tmp.pizza_name, pizzeria.name AS pizzeria_name, tmp.price FROM
  (SELECT * FROM menu
    WHERE pizza_name='mushroom pizza' OR pizza_name='pepperoni pizza') AS tmp
FULL JOIN pizzeria ON tmp.pizzeria_id = pizzeria.id WHERE tmp.pizza_name is NOT NULL
ORDER BY pizza_name, pizzeria_name
