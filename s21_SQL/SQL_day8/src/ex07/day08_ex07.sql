-- For Sesseion #1
BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- For Sesseion #2
BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- For Session #1
SHOW TRANSACTION ISOLATION LEVEL;
-- For Session #2
SHOW TRANSACTION ISOLATION LEVEL;
-- For Session #1
UPDATE pizzeria SET rating = 1 WHERE id = 1;
-- For Session #2
UPDATE pizzeria SET rating = 2 WHERE id = 2;
-- For Session #1
UPDATE pizzeria SET rating = 1 WHERE id = 2;
-- For Session #2
UPDATE pizzeria SET rating = 2 WHERE id = 1;
-- For Session #1
COMMIT;
-- For Session #2
COMMIT;
-- For Session #1
SELECT * FROM pizzeria;
-- For Session #2
SELECT * FROM pizzeria;