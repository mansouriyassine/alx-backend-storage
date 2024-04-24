-- Create a table users with the specified attributes if it doesn't already exist

-- Check if the table exists
IF NOT EXISTS (
    SELECT *
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
    AND table_name = 'users'
) THEN
    -- Create the table
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255),
        country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
    );
END IF;