SELECT order_date,
  (SELECT CONCAT(new.name, ' (age:', new.age, ')')) AS person_information
FROM person_order
NATURAL JOIN
(SELECT id AS person_id, name, age FROM person) AS new
ORDER BY order_date, person_information
