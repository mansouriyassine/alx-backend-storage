-- Create a stored procedure ComputeAverageScoreForUser

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Create the procedure
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;
    
    -- Calculate the total score for the user
    SELECT SUM(score) INTO total_score FROM corrections WHERE user_id = user_id;
    
    -- Calculate the total number of projects for the user
    SELECT COUNT(DISTINCT project_id) INTO total_projects FROM corrections WHERE user_id = user_id;
    
    -- Compute the average score
    IF total_projects > 0 THEN
        UPDATE users SET average_score = total_score / total_projects WHERE id = user_id;
    ELSE
        UPDATE users SET average_score = 0 WHERE id = user_id;
    END IF;
END //

DELIMITER ;