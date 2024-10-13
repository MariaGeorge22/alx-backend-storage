-- 6th Task
DROP TRIGGER IF EXISTS `new email`;

DELIMITER //
CREATE TRIGGER `new email`
BEFORE UPDATE ON `users`
FOR EACH ROW
BEGIN
IF NEW.email <> OLD.email THEN
SET NEW.valid_email = false;
END IF;
END//
DELIMITER ;
