-- Create an index idx_name_first_score on the first letter of the name column and the score column in the names table

CREATE INDEX idx_name_first_score
ON names(name(1), score);