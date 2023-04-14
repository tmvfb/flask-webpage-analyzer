DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name varchar(255) UNIQUE,
	created_at timestamp
);

INSERT INTO urls (name, created_at)
VALUES ('MY_NAME', '2023-04-14 12:00:00');
INSERT INTO urls (name, created_at)
VALUES ('YOUR_NAME', '2023-04-14 13:00:00');