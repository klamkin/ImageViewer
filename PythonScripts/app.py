#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response, session, send_from_directory
from flask_restful import Resource, Api
from flask_session import Session
import pymysql.cursors
import json
import hashlib
import os
from os.path import dirname, abspath
import cgitb
import cgi
import sys
import shutil
cgitb.enable()

import settings # Our server and db settings, stored in settings.py

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SESSION_TYPE'] = settings.SESSION_TYPE
app.config['SESSION_COOKIE_NAME'] = settings.COOKIE_NAME
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
app.config['PERMANENT_SESSION_LIFETIME'] = settings.SESSION_TIMEOUT
api = Api(app)
Session(app)


####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { "status": "Bad request" } ), 400)

@app.errorhandler(403) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status' : 'Access denied, need to include username and password, or sign in first' } ), 403)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "status": "Resource not found" } ), 404)

####################################################################################
#
# User authentication for pictures curl commands so that user doesn't have to hit signIn endpoint first
#
def authUser(username, password):
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
		sql = 'authUser'
		cursor = dbConnection.cursor()
		cursor.callproc(sql,(username, password)) # stored procedure, with arguments
		row = cursor.fetchone()

		if row == None:
			return False		
		else:
			#this code can be uncommented so a session will be created so a user doesn't have to reauthenticate until that session times out
			#session['username'] = username
			#session.modified = True
			#print(session)
			return True
	except:
		return False #exception occured while authenticating
	finally:
		cursor.close()
		dbConnection.close()

#
# This global method is used to construct the URLs that are returned from "GET" image requests, used in all 3 places, that's why it's global
#
def createPictureURLs(listOfDicts):
	#template: https://info3103.cs.unb.ca/<user-id>/INFO3103FinProj/pictureRoot/<username>/<pictureName>
	
	protocol = 'https://'
	hostname = settings.APP_HOST
	pathList = []

	for dictionary in listOfDicts:
		new_dict = {}			
		pictureName = dictionary['pictureName']
		picturePath = dictionary['picturePath']
		pictureUser = dictionary['username']
		new_dict['link'] = 'https://' + hostname + '/' + picturePath + '/' + pictureUser + '/' + pictureName
		pathList.append(new_dict)
		
	return pathList 

####################################################################################
#
# Static Endpoints for humans
#
class Root(Resource):
	# get method. What might others be aptly named? (hint: post)
	def get(self):
		return app.send_static_file('index.html')

api.add_resource(Root,'/')

class Developer(Resource):
	# get method. What might others be aptly named? (hint: post)
	def get(self):
		return send_static_file('developer.html')

api.add_resource(Developer,'/dev')

####################################################################################
#
# schools routing: GET and POST, individual school access
#
class Users(Resource):

	def deleteUser(self,username):
		
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteUser'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,[username,]) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
			shutil.rmtree("../pictureRoot/" + username)#this might have to change down the line
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

	def updateUser(self,username,newUsername):
		#need to add check for if there the newUsername is already taken
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateUser'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,(username,newUsername)) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
			os.rename("../pictureRoot/" + username,"../pictureRoot/" + newUsername)#this might have to change down the line
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

	def checkNameAvailability(self,newUsername):
		#need to add check for if there the newUsername is already taken
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'checkNameAvailability'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,[newUsername,]) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
			row = cursor.fetchone()
			if row == None:
				return True		
			else:
				return False
				
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		
	# POST: Create a new user
	def post(self):

		if not request.json or not 'username' in request.json or not 'password' in request.json:
			abort(400) # bad request

		username = request.json['username'];
		password = request.json['password'];

		if os.path.isdir("../pictureRoot/" + username):
			return make_response(jsonify( { "username" : username + " already exists"} ), 409)		
		else:
			try:
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				sql = 'createUser'
				
				cursor = dbConnection.cursor()
				cursor.callproc(sql,(username, password)) # stored procedure, with arguments
				dbConnection.commit() # database was modified, commit the changes
				os.makedirs("../pictureRoot/" + username)#this might have to change down the line
			except:
				abort(500) # Nondescript server error
			finally:
				cursor.close()
				dbConnection.close()
		return make_response(jsonify( { "username" : username + " successfully created"} ), 201) # Need to fix this to so that it returns properly. Could just return insert successful....

	# DELETE: Delete your account
	def delete(self):

		if not request.json and not 'username' in session:
			response = { 'status' : 'Access denied, need to include username and password, or sign in first' }
			responseCode = 403
			return make_response(jsonify(response), responseCode)
		
		if 'username' in session:
			Users.deleteUser(self,session['username'])
			response = { 'status' : 'User successfully deleted' }
			responseCode = 200
			session.pop("username")
		else:
			if not 'username' in request.json or not 'password' in request.json:
				response = { 'status' : 'Access denied, need to include username and password, or sign in first' }
				responseCode = 403
				return make_response(jsonify(response), responseCode)

			username = request.json['username'];
			password = request.json['password'];
		
			if authUser(username,password):
				Users.deleteUser(self,username)
				response = { 'status' : 'User successfully deleted' }
				responseCode = 200
			else:
				response = { 'status' : 'Access denied, invalid username/password' }
				responseCode = 403
		

		return make_response(jsonify(response), responseCode)

	# PUT: Update your account username 
	def put(self):

		if not request.json or not 'newUsername' in request.json:
			abort(400) # bad request
		
		newUsername = request.json['newUsername']

		if (not 'username' in request.json and not 'password' in request.json) and not 'username' in session:
			response = { 'status' : 'Access denied, need to include username and password, or sign in first' }
			responseCode = 403
			return make_response(jsonify(response), responseCode)
		
		if 'username' in session:
			if Users.checkNameAvailability(self,newUsername):
				Users.updateUser(self,session['username'], newUsername)
				response = { 'status' : 'Username successfully changed' }
				responseCode = 200
				session['username'] = newUsername
			else:
				response = { 'status' : 'Username already taken' }
				responseCode = 406
		else:
			username = request.json['username'];
			password = request.json['password'];
		
			if authUser(username,password):
				if Users.checkNameAvailability(self,newUsername):
					Users.updateUser(self,username, newUsername)
					response = { 'status' : 'Username successfully changed' }
					responseCode = 200
				else:
					response = { 'status' : 'Username already taken' }
					responseCode = 406
			else:
				response = { 'status' : 'Access denied, invalid username/password' }
				responseCode = 403
		

		return make_response(jsonify(response), responseCode)


class SignIn(Resource):
	#Sign in
	def post(self):
		#
		# Sample command line usage:
		#
		# curl -i -H "Content-Type: application/json" -X POST -d '{"Name": "abc", "Number": 23}' 192.168.56.101:xxxxx/users
		if not request.json or not 'username' in request.json or not 'password' in request.json:
			abort(400) # bad request

		username = request.json['username']; #might also have to get username and password in different way
		password = request.json['password'];
		
		if 'username' in session: #if we start getting sessions mixed up with one another, this might be a good spot to add something like 'if session['username'] == username'
			response = { "status" : session['username'] + " already logged in"}
			responseCode = 200;
		else:
			try:
				dbConnection = pymysql.connect(settings.DB_HOST,
					settings.DB_USER,
					settings.DB_PASSWD,
					settings.DB_DATABASE,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				sql = 'authUser'
				cursor = dbConnection.cursor()
				cursor.callproc(sql,(username, password)) # stored procedure, with arguments
				row = cursor.fetchone()

				if row == None:
					response = { 'status' : 'Access denied' }
					responseCode = 403		
				else:
					response = { "status" : username + " logged in successfully"}
					responseCode = 201;
					session['username'] = username
					session.modified = True 
			except:
				abort(500) # Nondescript server error
			finally:
				cursor.close()
				dbConnection.close()
		return make_response(jsonify(response), responseCode)

	#log out
	def delete(self): #May have to change this to be able to include username/password in json in some way, but I don't know of a way how today
		
		if 'username' in session:
			response = { "status" : session['username'] + " logged out successfully"}
			responseCode = 200;
			session.pop('username')
		else:

			response = { 'status' : 'Session doesn\'t exist' }
			responseCode = 403; #this response code probably isn't right

		return make_response(jsonify(response), responseCode)


class PictureRoot(Resource):

	def queryAllImages(self):
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getAllPictures'
			cursor = dbConnection.cursor()
			cursor.callproc(sql)
			rows = cursor.fetchall()

			return rows
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

	#Get all the pictures for every user
	def get(self):

		if not request.json and not 'username' in session:
			abort(400) # bad request
		
		if 'username' in session: 
			responseList = PictureRoot.queryAllImages(self)
			response = createPictureURLs(responseList)
			responseCode = 200
			return make_response(jsonify(response), responseCode) # 
		else:
			if not 'username' in request.json or not 'password' in request.json:
				abort(400) # bad request

			username = request.json['username']; #might also have to get username and password in different way
			password = request.json['password'];
			
			if authUser(username, password): #user is authenticated
				responseList = PictureRoot.queryAllImages(self)
				response = createPictureURLs(responseList)
				responseCode = 200
				return make_response(jsonify(response), responseCode) # 
			else: #authentication failed
				responseCode = 403
				response = 'Invalid login credentials'
				return make_response(jsonify(response), responseCode) # 

	
	
class UserPictures(Resource):
	
	def queryUserImages(self,username):
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getAllUserPictures'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,[username,])
			rows = cursor.fetchall()

			return rows
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

	def get(self,username): #will have to construct URI's to pictures on the fly here, will need to add a new method or something
		
		if not request.json and not 'username' in session:
			abort(400) # bad request
		
		#queryUsername = request.json['lookForUsername']
		queryUsername = username
	
		if 'username' in session: 
			responseList = UserPictures.queryUserImages(self,queryUsername)
			response = createPictureURLs(responseList)
			responseCode = 200
			return make_response(jsonify(response), responseCode)
		else:
			if not 'username' in request.json or not 'password' in request.json:
				abort(400) # bad request

			loginUsername = request.json['username'];
			password = request.json['password'];
			
			if authUser(loginUsername, password): #user is authenticated
				responseList = UserPictures.queryUserImages(self,queryUsername)
				response = createPictureURLs(responseList)
				responseCode = 200
				return make_response(jsonify(response), responseCode) # 
			else: #authentication failed
				responseCode = 403
				response = 'Invalid login credentials'
				return make_response(jsonify(response), responseCode) # 


class UserSpecificPictures(Resource):

	def allowed_file(self,filename):
		ALLOWED_EXTENSIONS = set(['jpg','jpeg','png'])
		return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
	
	def queryUserImage(self,username,pictureName):
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getSingleUserPicture'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,(username,pictureName))
			rows = cursor.fetchall()

			return rows
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

	def deletePicture(self,username,pictureName):
		try:
			#print(username + " " + pictureName)
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deletePicture'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,(username,pictureName))
			dbConnection.commit()
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

	def updatePictureName(self,username,pictureName,newPictureName):
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'updatePictureName'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,(username,pictureName,newPictureName))
			dbConnection.commit()
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

	def postNewPicture(self,username,pictureName,picturePath):
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'postNewPicture'
			cursor = dbConnection.cursor()
			cursor.callproc(sql,(username,pictureName,picturePath))
			dbConnection.commit()
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()	

	def get(self,username,pictureName): #will have to construct urls to pictures on the fly here

		if not request.json and not 'username' in session:
			abort(400) # bad request
		
		queryUsername = username
		queryPicture = pictureName		

		if 'username' in session: 
			responseList = UserSpecificPictures.queryUserImage(self,queryUsername,queryPicture)
			if len(responseList) == 0:
				responseCode = 404
				response = "status: Image does not exist"
				return make_response(jsonify(response), responseCode)
			response = createPictureURLs(responseList)
			responseCode = 200
			return make_response(jsonify(response), responseCode)
		else:
			if not 'username' in request.json or not 'password' in request.json:
				abort(400) # bad request

			loginUsername = request.json['username']; #might also have to get username and password in different way
			password = request.json['password'];
			
			if authUser(loginUsername, password): #user is authenticated
				responseList = UserSpecificPictures.queryUserImage(self,queryUsername,queryPicture)
				if len(responseList) == 0:
					responseCode = 404
					response = "status: Image does not exist"
					return make_response(jsonify(response), responseCode)
				response = createPictureURLs(responseList)
				responseCode = 200
				return make_response(jsonify(response), responseCode) # 
			else: #authentication failed
				responseCode = 403
				response = 'Invalid login credentials'
				return make_response(jsonify(response), responseCode) # 

	def delete(self,username,pictureName): #for this endpoint, where should we get the username from.... the URL or the json, my guess is JSON
		
		if not request.json and not 'username' in session:
			abort(400) # bad request
	
		queryPicture = pictureName		

		try:
			if 'username' in session:
				if UserSpecificPictures.queryUserImage(self,session['username'],queryPicture) != None: 
					os.remove('../pictureRoot/' + session['username'] + '/' + queryPicture)
					UserSpecificPictures.deletePicture(self,session['username'],queryPicture)
					responseCode = 200
					return make_response(jsonify("status:" + queryPicture + " was successfully deleted"), responseCode)
			else:
				if not 'username' in request.json or not 'password' in request.json:
					abort(400) # bad request

				loginUsername = request.json['username']; #might also have to get username and password in different way
				password = request.json['password'];
			
				if authUser(loginUsername, password): #user is authenticated
					if UserSpecificPictures.queryUserImage(self,loginUsername,queryPicture) != None:
						os.remove('../pictureRoot/' + loginUsername + '/' + queryPicture)
						UserSpecificPictures.deletePicture(self,loginUsername,queryPicture)
						responseCode = 200
						return make_response(jsonify("status:" + queryPicture + " was successfully deleted"), responseCode) #
				else: #authentication failed
					responseCode = 403
					response = 'Invalid login credentials'
					return make_response(jsonify(response), responseCode) #
		except:
			responseCode = 404
			return make_response(jsonify("status: " + queryPicture + " doesn't exist"), responseCode) 

	def put(self,username,pictureName):
		
		if not request.json or not 'newPictureName' in request.json:
			abort(400) # bad request
	
		queryPicture = pictureName		
		newPictureName = request.json['newPictureName']		

		try:
			if 'username' in session:
				if len(UserSpecificPictures.queryUserImage(self,session['username'],newPictureName)) == 0: 
					os.rename('../pictureRoot/' + session['username'] + '/' + queryPicture, '../pictureRoot/' + session['username'] + '/' + newPictureName)
					UserSpecificPictures.updatePictureName(self,session['username'],queryPicture,newPictureName)
					responseCode = 200
					response = "status:" + queryPicture + " was successfully changed to " + newPictureName
					return make_response(jsonify(response), responseCode)
				else:
					responseCode = 406
					response = "status: " + newPictureName + " is already used, please use a new one"
					return make_response(jsonify(response), responseCode)
			else:
				if not 'username' in request.json or not 'password' in request.json:
					abort(400) # bad request

				loginUsername = request.json['username']; #might also have to get username and password in different way
				password = request.json['password'];
			
				if authUser(loginUsername, password): #user is authenticated
					if len(UserSpecificPictures.queryUserImage(self,loginUsername,newPictureName)) == 0:
						os.rename('../pictureRoot/' + loginUsername + '/' + queryPicture, '../pictureRoot/' + loginUsername + '/' + newPictureName)
						UserSpecificPictures.updatePictureName(self,loginUsername,queryPicture,newPictureName)
						responseCode = 200
						response = "status:" + queryPicture + " was successfully changed to " + newPictureName
						return make_response(jsonify(response), responseCode) #
					else:
						responseCode = 406
						response = "status: " + newPictureName + " is already used, please use a new one"
						return make_response(jsonify(response), responseCode)
				else: #authentication failed
					responseCode = 403
					response = 'Invalid login credentials'
					return make_response(jsonify(response), responseCode) #
		except:
			abort(500) 

	def post(self,username,pictureName): #need to make sure to add check if the new name already exists
		
		if 'file' not in request.files:
			responseCode = 	400
			response = "status: No file specified for upload"
			return make_response(jsonify(response), responseCode)	

		newPicture = request.files['file']
		newPictureName = pictureName
		
		if newPictureName == '':
			responseCode = 	400
			response = "status: Must include new filename at end of URI"
			return make_response(jsonify(response), responseCode)

		if not UserSpecificPictures.allowed_file(self,newPictureName):
			responseCode = 	403
			response = "status: You cannot upload a file of this type"
			return make_response(jsonify(response), responseCode)
		
		try:
			fs_upload_folder = '../pictureRoot/'
			db_file_path_list = dirname(dirname(abspath(__file__))).split('/')
			db_file_path = db_file_path_list[len(db_file_path_list) - 1] + '/pictureRoot' #hardcoded in, can add programatic way to get directories if needed 
			
			if 'username' in session:
				if len(UserSpecificPictures.queryUserImage(self,session['username'],newPictureName)) == 0: 
					newPicture.save(os.path.join(fs_upload_folder,session['username'],newPictureName))
					UserSpecificPictures.postNewPicture(self,session['username'],newPictureName,db_file_path)
					responseCode = 201
					response = "status:" + newPictureName + " was successfully added"
					return make_response(jsonify(response), responseCode)
				else:
					responseCode = 406
					response = "status: " + newPictureName + " is already used, please rename the picture"
					return make_response(jsonify(response), responseCode)
			else:
				response = 'status: You need to have login using the users/signIn endpoint in order to post a photo'
				responseCode = 401
				return make_response(jsonify(response), responseCode)
		except:
			abort(500)


api = Api(app)
api.add_resource(Users, '/users') #this should really be looked at as well
api.add_resource(SignIn, '/users/signIn')
api.add_resource(PictureRoot, '/pictureRoot')
api.add_resource(UserPictures, '/pictureRoot/<string:username>')
api.add_resource(UserSpecificPictures,'/pictureRoot/<string:username>/pictures/<string:pictureName>')

if __name__ == "__main__":
	context = ('cert.pem','key.pem')
	app.run(host=settings.APP_HOST, port=settings.APP_PORT, ssl_context=context ,debug=settings.APP_DEBUG)
