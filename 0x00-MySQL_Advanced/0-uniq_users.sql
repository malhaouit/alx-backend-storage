-- This SQL script creates a table `users` with these attributes:
-- => id: integer - not null - auto increment - primary key
-- => email: string (255 characters)- not null - unique
-- => name: string (255 characters)

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255)
);
