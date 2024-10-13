-- 1st Optional Task
DROP PROCEDURE IF EXISTS `ComputeAverageWeightedScoreForUser`;
DELIMITER // 
CREATE PROCEDURE `ComputeAverageWeightedScoreForUser` (IN user_id INT) BEGIN
UPDATE `users`
SET average_score = (
		SELECT SUM(score * weight) / SUM(weight)
		FROM corrections
		JOIN projects
		ON projects.id = project_id
		WHERE corrections.user_id = user_id
		GROUP BY corrections.user_id
	) 
WHERE users.id = user_id;
END // 
DELIMITER ;
