DELIMITER //

CREATE PROCEDURE updateUser (IN usernameIN varchar(250),IN newUsernameIN varchar(250))
BEGIN
  UPDATE userInfo SET username = newUsernameIN WHERE username = usernameIN;
  UPDATE pictures SET username = newUsernameIN WHERE username = usernameIN;
END;
//

DELIMITER ;
