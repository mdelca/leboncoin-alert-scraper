begin;

CREATE TABLE alert(
    id_alert SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    url VARCHAR NOT NULL,
    last_check TIMESTAMP NOT NULL DEFAULT NOW());

CREATE TABLE "user"(
    id_user SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    phone VARCHAR);

CREATE TABLE subscription(
    id_subscription SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL REFERENCES "user",
    id_alert INTEGER NOT NULL REFERENCES "alert");
