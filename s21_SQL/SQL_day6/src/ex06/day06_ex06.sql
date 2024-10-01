CREATE SEQUENCE seq_person_discounts START WITH 1;
SELECT setval('seq_person_discounts', (SELECT COUNT(*) + 1 FROM person_discounts));
ALTER TABLE person_discounts ALTER id SET DEFAULT nextval('seq_person_discounts');