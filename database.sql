DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name varchar(255) UNIQUE,
	created_at timestamp
);

CREATE TABLE url_checks (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	url_id bigint REFERENCES urls(id),
	status_code int,
	h1 varchar(255),
	title varchar(255),
	description text,
	created_at timestamp
);

INSERT INTO urls (name, created_at)
VALUES ('MY_NAME', '2023-04-14 12:00:00');

INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
VALUES (1, 302, 'Hello', 'World', 'Hello world', '2023-04-14 13:00:00');