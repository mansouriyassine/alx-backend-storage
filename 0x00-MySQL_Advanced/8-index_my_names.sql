-- Create an index idx_name_first on the first letter of the name column in the names table

-- Drop the index if it already exists
DROP INDEX IF EXISTS idx_name_first ON names;

-- Create the index
CREATE INDEX idx_name_first ON names (LEFT(name, 1));