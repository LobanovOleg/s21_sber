WITH CTE(missing_date) AS (
  (SELECT days::DATE AS missing_date
    FROM generate_series('2022-01-01', '2022-01-10', interval '1 day') AS days))
SELECT missing_date FROM CTE
FULL JOIN
  (SELECT * FROM person_visits
    WHERE person_id = 1 OR person_id = 2 AND visit_date BETWEEN '2022-01-01' AND '2022-01-10') AS new
ON missing_date = new.visit_date WHERE new.person_id is NULL
ORDER BY missing_date
