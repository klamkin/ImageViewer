DELIMITER //

CREATE PROCEDURE updatePictureName (IN usernameIN varchar(250), IN pictureNameIN varchar(250), IN newPictureNameIN varchar(250))
BEGIN
  UPDATE pictures SET pictureName = newPictureNameIN WHERE username = usernameIN AND pictureName = pictureNameIN;
END;
//

DELIMITER ;
