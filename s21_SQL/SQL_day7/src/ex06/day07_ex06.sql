SELECT name,
       COUNT(person_order.id) AS count_of_orders,
       ROUND(AVG(menu.price), 0) AS averange_price,
       MAX(menu.price) AS max_price,
       MIN(menu.price) AS min_price
FROM pizzeria
JOIN menu ON menu.pizzeria_id = pizzeria.id
JOIN person_order ON person_order.menu_id = menu.id
GROUP BY 1
ORDER BY 1