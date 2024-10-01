CREATE TABLE nodes (
  point1 VARCHAR NOT NULL,
  point2 VARCHAR NOT NULL,
  cost INT NOT NULL
);

INSERT INTO
  nodes (point1, point2, cost)
VALUES 
  ('a', 'b', 10),
  ('b', 'a', 10),
  ('a', 'd', 20),
  ('d', 'a', 20),
  ('a', 'c', 15),
  ('c', 'a', 15),
  ('b', 'd', 25),
  ('d', 'b', 25),
  ('b', 'c', 35),
  ('c', 'b', 35),
  ('c', 'd', 30),
  ('d', 'c', 30);

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
ORDER BY
    total_cost,
    tour;
