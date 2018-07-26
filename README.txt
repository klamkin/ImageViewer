This project was done by Tycen Jardine and Kyle Lamkin.

Our API is an image file system, where you can post/update/delete images, as well as view your images as well as other peoples. The script that runs the API is called imageviewer.py and it is associated with a settings.py file.

This API can be accessed using cURL to send HTTP requests. The API allows you to.
	- Create an account
	- Update the name of that account
	- Delete that account
	- Sign in
	- Log out
	- View images of all users
	- View all images of a specific user
	- View a specific image of a user
	- Delete one of your images
	- Update the name of one of your images
	- Post a new image

Side note: Currently the pictureRoot directory is housed in the PythonScripts directory. The pictureRoot directory holds all of our pictures for each user. This directory will be brought out of PythonScripts for final deliverable. However, everything works.

SETUP:

1. Download FinalWeb.tar.gz
2. SCP the tar.gz file over to info3103.cs.unb.ca to YOUR USERNAME directory (IMPORTANT) ie for me, it's tjardin1
3. SSH onto info3103.cs.unb.ca, and go to the directory of your username where FinalWeb.tar.gz is located
4. Extract the tar.gz file
5. cd into PythonScripts
6. In the SQLScripts directory, there is all of the sql scripts that you will need to set up the database.
7. Login to MariaDB, create a database, and run the sql scripts. Be sure to run "RunLast.sql" last, since it uses stored procedures to insert dummy data.
8. Once that is done, go to the PythonScripts directory, and start imageviewer.py
9. Go to the originally downloaded tar file that you got from d2l on your local machine, unzip the directory, and go to the ClientSide directory.
10. Start the driver.sh script until completion, each endpoint in the API should be hit in the process

