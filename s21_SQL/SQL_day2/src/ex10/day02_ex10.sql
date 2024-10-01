SELECT
  person_1.name as person_name1,
  person_2.name as person_name2,
  person_1.address as commom_address
FROM person AS person_1
CROSS JOIN person AS person_2
WHERE person_1.name != person_2.name AND person_1.address = person_2.address AND person_1.id > person_2.id
ORDER BY 1, 2, 3
