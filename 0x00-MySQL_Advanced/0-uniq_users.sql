-- Create a table users with unique email constraint

-- If the table exists, drop it
DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);