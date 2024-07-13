-- Create the AddBonus stored procedure
DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;

    -- Check if the project exists and get the project_id
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name
    LIMIT 1;

    -- If the project does not exist, create it and get the new project_id
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END //

DELIMITER ;
