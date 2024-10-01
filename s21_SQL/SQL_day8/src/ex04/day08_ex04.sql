-- For Sessoin #1
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- For Session #2
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- For Session #1
SHOW TRANSACTION ISOLATION LEVEL;
-- For Session #2
SHOW TRANSACTION ISOLATION LEVEL;
-- For Session #1
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';
-- For Session #2
UPDATE pizzeria SET rating = 3.0 WHERE name = 'Pizza Hut';
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