DELIMITER //

CREATE PROCEDURE createUser (IN usernameIN varchar(250), IN userpassIN varchar(250))
BEGIN
  INSERT INTO userInfo (username, userpass) VALUES (usernameIN,SHA2(userpassIN,512));
END;
//

DELIMITER ;
