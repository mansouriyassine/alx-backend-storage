-- Create a trigger to decrease item quantity after adding a new order

-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS decrease_quantity_trigger;

-- Create the trigger
CREATE TRIGGER decrease_quantity_trigger AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the quantity of the item in the items table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;