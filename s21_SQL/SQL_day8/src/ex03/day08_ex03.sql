-- For Session #1
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- For Session #2
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- For Session #1
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';
-- For Session #2
UPDATE pizzeria SET rating = 3.6 WHERE name = 'Pizza Hut';
-- For Session #2
COMMIT;
-- For Session #1
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';
-- For Session #1
COMMIT;
-- For Session #1
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';
-- For Session #2
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';