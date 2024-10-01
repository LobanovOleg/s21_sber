SELECT address,
       ROUND(MAX(AGE) - 1.0 * MIN(AGE) / MAX(AGE), 2) AS formula,
       ROUND(AVG(AGE), 2) AS average,
       ROUND(MAX(AGE) - MIN(AGE) / MAX(AGE), 2) > ROUND(AVG(AGE), 2) AS compare
FROM person
GROUP BY address
ORDER BY address