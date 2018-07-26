DELIMITER //

CREATE PROCEDURE getAllPictures ()
BEGIN
  SELECT picturePath,username,pictureName FROM pictures;
END;
//

DELIMITER ;
