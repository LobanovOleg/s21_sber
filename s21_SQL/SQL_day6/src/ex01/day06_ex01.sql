INSERT INTO person_discounts (id, person_id, pizzeria_id, discount)
SELECT ROW_NUMBER() OVER() AS
    id, person.id AS person_id, pizzeria.id AS pizzeria_id,
    CASE 
        WHEN COUNT(person_order.id) = 1 THEN 10.5
        WHEN COUNT(person_order.id) = 2 THEN 22 
        ELSE  30
    END AS discount
FROM person_order
JOIN menu ON person_order.menu_id = menu.id
JOIN person ON person_order.person_id = person.id
JOIN pizzeria ON menu.pizzeria_id = pizzeria.id
GROUP BY 2, 3
ORDER BY 2, 3