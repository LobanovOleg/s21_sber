--For Session #1
BEGIN;
UPDATE pizzeria SET rating = 5 WHERE name = 'Pizza Hut';
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';

--For Session #2
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';

--For Session #1
COMMIT;

--For Session #2
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';