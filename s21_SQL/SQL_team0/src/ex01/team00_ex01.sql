WITH RECURSIVE
    path (passed, last_point, total_cost) AS (
        SELECT
            point1 || ',' || point2,
            point2,
            cost
        FROM
            nodes AS n
        WHERE
            point1 = 'a'

        UNION

        SELECT
          path.passed || ',' || n.point2,
          n.point2,
          path.total_cost + n.cost
        FROM
            path

        JOIN
            nodes AS n ON
                path.last_point = n.point1

        WHERE
            (POSITION(n.point2 IN path.passed) = 0) OR   -- еще не посетили вершину
                (LENGTH(path.passed) = 7 AND             -- посетили ровно 5 вершин и возвращаемся в a
                POSITION(n.point2 IN path.passed) = 1)
        ),
    ok_path AS (
        SELECT *
        FROM
            path
        WHERE
            LENGTH(path.passed) = 9
    )

SELECT
    total_cost,
    ('{' || passed || '}') AS tour
FROM
    ok_path
WHERE
    total_cost = (
        SELECT
            MIN(total_cost)
        FROM ok_path
        )
    OR
        total_cost = (
        SELECT
            MAX(total_cost)
        FROM ok_path
        )
ORDER BY
    total_cost,
    tour;