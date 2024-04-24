-- Create a stored procedure ComputeAverageWeightedScoreForUsers that computes and stores the average weighted score for all students.

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Delimiter to handle the procedure creation
DELIMITER //

-- Create the procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_score FLOAT;

    -- Cursor to iterate over users
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Start processing each user
    user_loop: LOOP
        -- Fetch the next user ID
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Initialize total score and total weight for the user
        SET total_score = 0;
        SET total_weight = 0;

        -- Calculate the total weighted score for the user
        SELECT SUM(corrections.score * projects.weight)
        INTO total_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate the total weight of all projects
        SELECT SUM(weight)
        INTO total_weight
        FROM projects;

        -- Calculate the average weighted score for the user
        IF total_weight > 0 THEN
            SET avg_score = total_score / total_weight;
        ELSE
            SET avg_score = 0;
        END IF;

        -- Update the average score for the user
        UPDATE users
        SET average_score = avg_score
        WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END //

-- Reset the delimiter
DELIMITER ;