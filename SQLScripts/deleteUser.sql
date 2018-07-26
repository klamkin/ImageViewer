DELIMITER //

CREATE PROCEDURE deleteUser (IN usernameIN varchar(250))
BEGIN
  DELETE FROM pictures WHERE username = usernameIN;
  DELETE FROM userInfo WHERE username = usernameIN;
END;
//

DELIMITER ;
