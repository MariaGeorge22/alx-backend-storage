-- 7th Task
DROP PROCEDURE IF EXISTS `AddBonus`;

DELIMITER // 
CREATE PROCEDURE `AddBonus` (
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score INT
) BEGIN
DECLARE project_id int;
IF project_name NOT IN (
	SELECT DISTINCT (name)
	FROM `projects`
) THEN
INSERT INTO `projects` (name)
VALUES (project_name);
END IF;
SET project_id = (
		SELECT (id)
		FROM `projects`
		WHERE project_name = name
);
INSERT INTO `corrections` (user_id, project_id, score) 
VALUES (user_id, project_id, score);
END// 
DELIMITER ;
