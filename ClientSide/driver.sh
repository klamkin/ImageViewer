#!/bin/bash
declare -i port=44746
# Read username and password
echo "Create a new account"
read -p "ip/domain name: " ip
read -p "username: " username
read -s -p "password: " password

# Create user
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"'$username'","password":"'$password'"}' -c cookie-jar -b cookie-jar -k https://$ip:$port/users

# User Log In
echo "Log in with the account you just made"
read -p "username: " username
read -s -p "password: " password

curl -i -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}' -c cookie-jar -b cookie-jar -k https://$ip:$port/users/signIn

# Posting an Image
curl -i -H "Content-Type: multipart/form-data" -X POST -c cookie-jar -b cookie-jar -F 'file=@image2.jpg' -k https://$ip:$port/pictureRoot/$username/pictures/image2.jpg

#Get all images
curl -i -X GET -c cookie-jar -b cookie-jar -k https://$ip:$port/pictureRoot

#Get all images for specific user
curl -i -X GET -c cookie-jar -b cookie-jar -k https://$ip:$port/pictureRoot/$username

#Change name of picture
echo "Change the name of the picture you just posted (add .jpg for extension)"
read -p "new picture name: " newPictureName

curl -i -H "Content-Type: application/json" -X PUT -d '{"newPictureName": "'$newPictureName'"}' -c cookie-jar -b cookie-jar -k https://$ip:$port/pictureRoot/$username/pictures/image1.jpg

# Get specific image
curl -i -X GET -c cookie-jar -b cookie-jar -k https://$ip:$port/pictureRoot/$username/pictures/$newPictureName

# Changing username
echo "Change your username"
read -p "New username: " newUsername

curl -i -H "Content-Type: application/json" -X PUT -d '{"newUsername":"'$newUsername'"}' -c cookie-jar -b cookie-jar -k https://$ip:$port/users

# Delete image
curl -i -X DELETE -c cookie-jar -b cookie-jar -k https://$ip:$port/pictureRoot/$newUsername/pictures/$newPictureName

# Log out
curl -i -X DELETE -c cookie-jar -b cookie-jar -k https://$ip:$port/users/signIn

# Delete user
curl -i -H "Content-Type: application/json" -X DELETE -d '{"username": "'$newUsername'", "password": "'$password'"}' -k https://$ip:$port/users
