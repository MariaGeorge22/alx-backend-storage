-- 12th Task
DROP VIEW IF EXISTS `need_meeting`;

CREATE VIEW `need_meeting` (name)
AS (
	SELECT (name) from students
	WHERE score < 80 AND (
		last_meeting IS NULL
		OR
		last_meeting < DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
		)
);
