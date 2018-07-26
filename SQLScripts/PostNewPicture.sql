DELIMITER //

CREATE PROCEDURE postNewPicture (IN usernameIN varchar(250), IN pictureNameIN varchar(250), IN picturePathIN varchar(250))
BEGIN
  INSERT INTO pictures (picturePath,username,pictureName) VALUES (picturePathIN,usernameIN, pictureNameIN);
END;
//

DELIMITER ;
