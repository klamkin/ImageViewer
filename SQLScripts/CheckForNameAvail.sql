DELIMITER //

CREATE PROCEDURE checkNameAvailability (IN newUsernameIN varchar(250))
BEGIN
  SELECT username FROM userInfo WHERE username = newUsernameIN;
END;
//

DELIMITER ;
