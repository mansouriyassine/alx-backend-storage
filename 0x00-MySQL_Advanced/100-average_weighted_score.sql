-- Create a stored procedure ComputeAverageWeightedScoreForUser that computes and stores the average weighted score for a student.

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Delimiter to handle the procedure creation
DELIMITER //

-- Create the procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_score FLOAT;

    -- Calculate the total weighted score
    SELECT SUM(corrections.score * projects.weight)
    INTO total_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the total weight
    SELECT SUM(weight)
    INTO total_weight
    FROM projects;

    -- Calculate the average weighted score
    IF total_weight > 0 THEN
        SET avg_score = total_score / total_weight;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the average score for the user
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //

-- Reset the delimiter
DELIMITER ;