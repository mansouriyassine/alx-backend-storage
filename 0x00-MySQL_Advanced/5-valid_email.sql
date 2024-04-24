-- Create a trigger to reset valid_email attribute when email is changed

-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS reset_valid_email_trigger;

-- Create the trigger
CREATE TRIGGER reset_valid_email_trigger BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;