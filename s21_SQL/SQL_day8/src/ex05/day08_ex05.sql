-- For Sesseion #1
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- For Sesseion #2
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- For Session #1
SHOW TRANSACTION ISOLATION LEVEL;
-- For Session #2
SHOW TRANSACTION ISOLATION LEVEL;
-- For Session #1
SELECT SUM(rating) FROM pizzeria;
-- For Session #2
UPDATE pizzeria SET rating = 1 WHERE name = 'Pizza Hut';
-- For Session #2
COMMIT;
-- For Session #1
SELECT SUM(rating) FROM pizzeria;
-- For Session #1
COMMIT;
-- For Session #1
SELECT SUM(rating) FROM pizzeria;
-- For Session #2
SELECT SUM(rating) FROM pizzeria;