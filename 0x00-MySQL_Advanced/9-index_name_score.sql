-- Create an index idx_name_first_score on the first letter of the name column and the score column in the names table

-- Drop the index if it already exists
DROP INDEX IF EXISTS idx_name_first_score ON names;

-- Create the index
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);