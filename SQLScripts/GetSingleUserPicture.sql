DELIMITER //

CREATE PROCEDURE getSingleUserPicture (IN usernameIN varchar(250), IN pictureNameIN varchar(250))
BEGIN
  SELECT picturePath,username,pictureName FROM pictures WHERE username = usernameIN AND pictureName = pictureNameIN;
END;
//

DELIMITER ;
