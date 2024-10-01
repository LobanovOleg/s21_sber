CREATE OR REPLACE FUNCTION fnc_fibonacci(IN pstop INTEGER DEFAULT 10)
RETURNS TABLE(num integer) AS $$
    WITH RECURSIVE CTE(num1, num2) AS (
        VALUES (0, 1)
        UNION ALL
            SELECT GREATEST(num1, num2), num1 + num2
        FROM CTE WHERE num2 < pstop
    )
    SELECT num1 FROM CTE;
$$ LANGUAGE sql;

SELECT * FROM fnc_fibonacci(100);
SELECT * FROM fnc_fibonacci();