DELIMITER //

CREATE PROCEDURE getAllUserPictures (IN usernameIN varchar(250))
BEGIN
  SELECT picturePath,username,pictureName FROM pictures WHERE username = usernameIN;
END;
//

DELIMITER ;
