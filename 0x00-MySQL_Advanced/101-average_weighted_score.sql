-- 1st Optional Task
DROP PROCEDURE IF EXISTS `ComputeAverageWeightedScoreForUsers`;

DELIMITER // 

CREATE PROCEDURE `ComputeAverageWeightedScoreForUsers` () 
BEGIN


CREATE TEMPORARY table `averages` AS (
		SELECT corrections.user_id AS user_id,
		SUM(score * weight) / SUM(weight) AS avg_score
		FROM corrections
		JOIN projects
		ON projects.id = project_id
		JOIN users
		ON users.id = user_id
		GROUP BY corrections.user_id
	);

UPDATE `users`
SET average_score = (
		SELECT avg_score 
		FROM `averages`
		WHERE id = user_id
	);

DROP TEMPORARY TABLE `averages`;
END // 

DELIMITER ;
