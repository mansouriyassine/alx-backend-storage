-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS decrease_quantity_trigger;

-- Create a trigger to decrease item quantity after adding a new order
DELIMITER //
CREATE TRIGGER decrease_quantity_trigger AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END//
DELIMITER ;

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS items (
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS orders (
    item_name VARCHAR(255) NOT NULL,
    number INT NOT NULL
);

-- Insert initial data into the items table
INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");