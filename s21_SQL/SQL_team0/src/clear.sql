DO $$
DECLARE
    tabname text;
BEGIN
    FOR tabname IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
    LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || tabname || ' CASCADE';
    END LOOP;
END $$;
