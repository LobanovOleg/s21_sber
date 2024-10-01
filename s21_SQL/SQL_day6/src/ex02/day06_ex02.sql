SELECT person.name AS person_name, menu.pizza_name, menu.price,
    ROUND(menu.price - menu.price * (person_discounts.discount / 100), 0) AS discount,
    pizzeria.name AS pizzeria_name
FROM person_order
JOIN person ON person_order.person_id = person.id
JOIN menu ON person_order.menu_id = menu.id
JOIN pizzeria ON menu.pizzeria_id = pizzeria.id
JOIN person_discounts ON person_discounts.person_id = person.id AND person_discounts.pizzeria_id = pizzeria.id
ORDER BY person_name, pizza_name