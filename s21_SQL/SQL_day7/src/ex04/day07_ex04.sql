SELECT person.name, COUNT(person_visits.id) AS count_of_visits
FROM person
JOIN person_visits ON person_visits.person_id = person.id
GROUP BY 1
HAVING COUNT(person_visits.id) > 3