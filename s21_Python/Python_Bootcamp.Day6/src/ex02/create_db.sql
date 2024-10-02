CREATE TABLE ships (
    ship_id SERIAL PRIMARY KEY,
    ship_name VARCHAR(100),
    alignment INTEGER,
    latitude_h INT,
    latitude_m INT,
    latitude_s FLOAT,
    longitude_h INT,
    longitude_m INT,
    longitude_s FLOAT
);

CREATE TABLE crew_members (
    member_id SERIAL PRIMARY KEY,
    ship_id INT REFERENCES ships(ship_id),
    ship_name VARCHAR(100),
    alignment INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    rank VARCHAR(50)
);

CREATE TABLE list_traitors (
    traitor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    rank VARCHAR(50)
);

DROP TABLE list_traitors;
DROP TABLE crew_members;
DROP TABLE ships;

psql -U lowban -d db_for_ship