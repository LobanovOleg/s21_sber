CREATE TABLE person_discounts (
    id BIGINT PRIMARY KEY,
    person_id BIGINT,
    pizzeria_id BIGINT,
    constraint fk_person_discounts_person_id FOREIGN KEY (person_id) REFERENCES person(id),
    constraint fk_person_discounts_pizzeria_id FOREIGN KEY (pizzeria_id) REFERENCES pizzeria(id),
    discount numeric(8, 1)
)