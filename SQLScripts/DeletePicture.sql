DELIMITER //

CREATE PROCEDURE deletePicture (IN usernameIN varchar(250), IN pictureNameIN varchar(250))
BEGIN
  DELETE FROM pictures WHERE username = usernameIN AND pictureName = pictureNameIN;
END;
//

DELIMITER ;
