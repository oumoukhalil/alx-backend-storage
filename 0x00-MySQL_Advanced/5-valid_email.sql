-- trigger
-- update de mail
DELIMITER |
CREATE TRIGGER update_mail BEFORE UPDATE ON users
FOR EACH ROW
	BEGIN
		SET NEW.valid_email = IF(NEW.email REGEXP '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$', 1, 0);
	END;
|
DELIMITER ;
