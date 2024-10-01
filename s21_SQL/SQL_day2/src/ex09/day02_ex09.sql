WITH
    CTE_pep(pepperoni) AS (
      (SELECT person.name AS pepperoni
        FROM person_order
        INNER JOIN person ON person_order.person_id = person.id
        INNER JOIN menu ON menu.id = person_order.menu_id
        WHERE person.gender = 'female' AND pizza_name = 'pepperoni pizza')
      ),
    CTE_che(cheese) AS (
      (SELECT person.name AS cheese
        FROM person_order
        INNER JOIN person ON person_order.person_id = person.id
        INNER JOIN menu ON menu.id = person_order.menu_id
        WHERE person.gender = 'female' AND pizza_name = 'cheese pizza')
      )
SELECT person.name FROM person
INNER JOIN CTE_pep ON CTE_pep.pepperoni = person.name
INNER JOIN CTE_che ON CTE_che.cheese = person.name
ORDER BY name
