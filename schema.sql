-- i found a csv online with the data i wanted it has a CCO 1.0 license, 
-- https://www.kaggle.com/mrdew25/pokemon-database
-- converted it to sqlite with sqlite tools via the command prompt

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
-- admind user
INSERT INTO users (user_id, password)
VALUES
  ('Admin', 'pbkdf2:sha256:260000$w07qrnYQh52uoWmR$ec16f2fbabeb429798953c1a84584e56075ffd752d7309a8a28bb7a882ad714e');
-- adminn user favourites
DROP TABLE IF EXISTS Admin_favourites;

CREATE TABLE Admin_favourites
(
    pokemon_id INTEGER PRIMARY KEY, 
    pokedex_number INTEGER NOT NULL, 
    pokemon_name TEXT NOT NULL, 
    alternate_form_name TEXT
);

-- DROP TABLE IF EXISTS Admin_teams;

-- CREATE TABLE Admin_teams
-- (
--     pokemon_id INTEGER PRIMARY KEY,
--     pokedex_number INTEGER NOT NULL,
--     pokemon_name TEXT NOT NULL,
--     alternate_form_name TEXT,
--     primary_type TEXT NOT NULL,
--     secondary_type TEXT
-- );