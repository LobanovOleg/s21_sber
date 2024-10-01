-- For Session #1
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- For Session #2
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- For Session #1
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';
-- For Session #2
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';
-- For Session #1
UPDATE pizzeria SET rating = 4 WHERE name = 'Pizza Hut';
-- For Session #1
COMMIT;
-- For Session #2
UPDATE pizzeria SET rating = 3.6 WHERE name = 'Pizza Hut';
-- For Session #2
COMMIT;
-- For Session #1
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';
-- For Session #2
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';