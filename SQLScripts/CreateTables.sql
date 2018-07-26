CREATE TABLE userInfo (
	userID int NOT NULL AUTO_INCREMENT,
	username varchar(250),
	userpass varchar(250),
	PRIMARY KEY (userID));


CREATE TABLE pictures (
	pictureID int NOT NULL AUTO_INCREMENT,
	picturePath varchar(250),
	username varchar(250),
	pictureName varchar(250),
	PRIMARY KEY (pictureID));

