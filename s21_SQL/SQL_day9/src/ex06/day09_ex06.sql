CREATE OR REPLACE FUNCTION fnc_person_visits_and_eats_on_date(
                                                              IN pperson varchar DEFAULT 'Dmitriy',
                                                              IN pprice numeric DEFAULT 500,
                                                              IN pdate date DEFAULT '2022-01-08')
RETURNS TABLE (
    name varchar
) AS $$
    BEGIN
        RETURN QUERY
            SELECT pizzeria.name FROM person_visits
            INNER JOIN person_order ON person_order.person_id = person_visits.id
            INNER JOIN pizzeria ON person_visits.pizzeria_id = pizzeria.id
            INNER JOIN menu ON person_order.menu_id = menu.id AND menu.pizzeria_id = pizzeria.id
            INNER JOIN person ON person_order.person_id = person.id AND person_visits.person_id = person.id
            WHERE person.name = pperson AND visit_date = pdate AND price < pprice;
    END;
$$ LANGUAGE plpgsql;

SELECT * FROM fnc_person_visits_and_eats_on_date(pprice := 800);
SELECT * FROM fnc_person_visits_and_eats_on_date(pperson := 'Anna', pprice := 1300, pdate := '2022-01-01');
