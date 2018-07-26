DELIMITER //

CREATE PROCEDURE authUser (IN usernameIN varchar(250), IN userpassIN varchar(250))
BEGIN
  SELECT * FROM userInfo where username = usernameIN AND userpass = SHA2(userpassIN,512);
END;
//

DELIMITER ;
