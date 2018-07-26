angular.module('IndexJS', [])
   .controller('SigninController', ['$scope', '$http', '$compile', function($scope, $http, $compile) {
     $scope.logUser = ''
     $scope.logPass = ''

     $scope.uploadFile= function(files) {
       var fd = new FormData();

       fd.append("file", files[0]);

       $http.post('https://info3103.cs.unb.ca:44746/pictureRoot/'+$scope.logUser+'/pictures/'+files[0].name, fd, {
         withCredentials: true,
         headers: {'Content-Type': undefined },
         transformRequest: angular.identity
       }).then(function(data) {

       });
     };

     $scope.returnLog = function (){
       $scope.logUser = ''
       $scope.logPass = ''
       $scope.message = '';
       $scope.message2 = '';
       $scope.message3 = '';
       $scope.userPics = true;
       $scope.hideLog = false;
       $scope.afterLog = true;
       $scope.hidePic = true;
       $scope.upload = false;
       $scope.home = true;
       $scope.profile = false;
       $scope.allPics = false;
       $scope.cleared = false;
       $scope.clearedAll = false;
       $scope.initialLoad = false;
       $scope.clearPics();
       //location.reload();
     }

	   $scope.message = '';
     $scope.message2 = '';
     $scope.message3 = '';
     $scope.userPics = true;
     $scope.hideLog = false;
     $scope.afterLog = true;
     $scope.hidePic = true;
     $scope.upload = false;
     $scope.home = true;
     $scope.profile = false;
     $scope.allPics = false;
     $scope.cleared = false;
     $scope.clearedAll = false;
     $scope.initialLoad = false;

     $scope.closePic = function (){
       /*document.getElementById('overImage').style.zIndex = "10";*/
       $('#imageOver1 div').empty();
     }

     $scope.clickPic = function (link){

       var add = "closePic()";
       var newEle = angular.element('<a class="centered" id="overImage"> <img id="derp" ng-click="'+add+'"src="'+link+'" width="1500" height="1000"> </a>');
       var target = document.getElementById('imageOver');
       var temp = $compile(newEle)($scope);
       angular.element(target).append(temp);
       document.getElementById('overImage').style.zIndex = "10";
     }

     $scope.changeUser = function (newName){
       credentials = JSON.stringify({"newUsername": newName});

       $http.put('https://info3103.cs.unb.ca:44746/users', credentials).then(function(data){
         $scope.message2 = data.status;
         if(data.status == 201 || data.status == 200)
         {
           $scope.message2 = 'Username Sucessfully Changed to: ' + newName;
         }
       })
       .catch(function(e){
         if(e.status == 400){
           $scope.message2 = "Bad Request"
         }
         else if(e.status == 403){
           $scope.message2 = "Not properly logged in to change username"
         }
         else if(e.status == 406){
           $scope.message2 = "Username already taken"
         }
       });
     }

     $scope.clearPics = function (){
       $('#target a').empty();
       $('#allTarget a').empty();
     }

     $scope.logOutFunc = function(){
       $http.delete('https://info3103.cs.unb.ca:44746/users/signIn').then(function(responce){

       });
       $scope.homeFunc();
       $scope.returnLog();
     }

     $scope.deleteUser = function (pass){
       credentials = JSON.stringify({"username": $scope.logUser, "password": pass});
       if(pass == $scope.logPass)
       {
         $http.delete('https://info3103.cs.unb.ca:44746/users', credentials).then(function(responce){
           $scope.homeFunc();
           $scope.returnLog();
         })
         .catch(function(e){
           if(e.status == 400){
             $scope.message3 = "Bad Request"
           }
           else if(e.status == 403){
             $scope.message3 = "Invalid Username or Password"
           }
           else if(e.status == 500){
             $scope.message3 = "Server Error"
           }
         });
       }
       else {
         $scope.message3 = "Invalid Password"
       }
     }

     $scope.removeActive = function (){
       $('#home').removeClass("active");
       $('#upload').removeClass("active");
       $('#profile').removeClass("active");
       $('#allPics').removeClass("active");
       $('#logOut').removeClass("active");
     }

     $scope.uploadFunc = function (){
       if ($scope.upload == false)
       {
         $scope.removeActive();
         document.getElementById("upload").classList.add('active');
         $scope.cleared = true;
         $scope.clearedAll = true;
         $scope.upload = true;
         $scope.home = false;
         $scope.profile = false;
         $scope.allPics = false;
         $scope.clearPics();
       }
     };
     $scope.homeFunc = function (){
       if ($scope.home == false)
       {
         if ($scope.cleared == true)
         {
           $scope.cleared = false;
           $scope.loadUserPics();
         }
         $scope.removeActive();
         document.getElementById("home").classList.add('active');
         $scope.upload = false;
         $scope.home = true;
         $scope.profile = false;
         $scope.allPics = false;
       }
     };
     $scope.profileFunc = function (){
       if ($scope.profile == false)
       {
         $scope.removeActive();
         document.getElementById("profile").classList.add('active');
         $scope.upload = false;
         $scope.home = false;
         $scope.profile = true;
         $scope.allPics = false;
       }
     };
     $scope.allPicsFunc = function (){
       if ($scope.allPics == false)
       {
         $scope.removeActive();
         document.getElementById("allPics").classList.add('active');
         $scope.upload = false;
         $scope.home = false;
         $scope.profile = false;
         $scope.allPics = true;
         if ($scope.clearedAll == true)
         {
           $scope.clearedAll = false;
           $scope.loadAllPics();
         }
         else if($scope.initialLoad == false)
         {
           $scope.initialLoad = true;
           $scope.loadAllPics();

         }
       }
     };

     var split = function (str) {
       return str.split('\\').pop().split('/').pop();
     }

     $scope.delPic = function (name){
       $http.delete('https://info3103.cs.unb.ca:44746/pictureRoot/' + $scope.logUser + '/pictures/' + name).then(function(responce){

       });
       $scope.clearPics();
       $scope.loadUserPics();
     };



     $scope.loadUserPics = function (){
       $http.get('https://info3103.cs.unb.ca:44746/pictureRoot/'  + $scope.logUser).then(function(responce){
         for (i = 0; i < responce.data.length; i++) {
           var str = "hello";
           str = split(responce.data[i].link);
           var add = "delPic('"+str+"')";
           var add2 = "clickPic('"+responce.data[i].link+"')";
           var newEle = angular.element('<a class="imageWrap"> <img ng-click="'+add2+'"src="'+responce.data[i].link+'" alt="Fjords" width="450" height="250"> <input type="button" class="delButton" value="X" ng-click="'+add+'"/> </a>');
           //var newEle = angular.element('<td align="center" valign="center"> <img src="' + responce.data[i].link + '" width="600" height="500" > <br /> ' + i + ' </ td>');
           var target = document.getElementById('target');
           var temp = $compile(newEle)($scope);
           angular.element(target).append(temp);
           //$compile(angular.element(target))(scope);
         }
       });
     };

     $scope.loadAllPics = function (){
       $http.get('https://info3103.cs.unb.ca:44746/pictureRoot').then(function(responce){
         for (i = 0; i < responce.data.length; i++) {
           var str = "hello";
           str = split(responce.data[i].link);
           var add = "delPic('"+str+"')";
           var add2 = "clickPic('"+responce.data[i].link+"')";
           var newEle = angular.element('<a class="imageWrap"> <img ng-click="'+add2+'"src="'+responce.data[i].link+'" alt="Fjords" width="450" height="250"> </a>');
           //var newEle = angular.element('<td align="center" valign="center"> <img src="' + responce.data[i].link + '" width="600" height="500" > <br /> ' + i + ' </ td>');
           var target = document.getElementById('allTarget');
           var temp = $compile(newEle)($scope);
           angular.element(target).append(temp);
           //$compile(angular.element(target))(scope);
         }
       });
     };

	   $scope.signin = function (user){
		   credentials = JSON.stringify({"username": user.username, "password": user.password});
		   // Submit the credentials
		   $http.post('https://info3103.cs.unb.ca:44746/users/signIn', credentials ).then(function(data) {
			   // Success here means the transmission was successful - not necessarily the login.
			   // The data.status determines login success
			   if(data.status == 201 || data.status == 200) {
          $scope.logUser = user.username;
          $scope.logPass = user.password;
					$scope.message = 'User successfully logged in';
          $scope.upload = false;
          $scope.hideLog = true;
          $scope.afterLog = false;
          $scope.userPics = false;
          $scope.loadUserPics();
          }

		   })
       .catch(function(e){
         if(e.status == 400){
           $scope.message = "Bad Request"
         }
         else if(e.status == 403){
           $scope.message = "Invalid Username or Password"
         }
         else if(e.status == 500){
           $scope.message = "Server Error"
         }
       });
	   }

		$scope.createUser = function (user){
			credentials = JSON.stringify({"username": user.username, "password": user.password});
			// Submit the credentials
			$http.post('https://info3103.cs.unb.ca:44746/users', credentials ).then(function(data) {
					// Success here means the transmission was successful - not necessarily the login.
					// The data.status determines login success
					console.log(data.status)
					if(data.status == 201) {
						// You're in!
						// But does the session carry? Let's try some other endpoint that requires a login
						$scope.signin(user);

				   }
				})
        .catch(function(e){
          if(e.status == 400){
            $scope.message = "Bad Request"
          }
          else if(e.status == 409){
            $scope.message = "Username Already Taken"
          }
          else if(e.status == 500){
            $scope.message = "Server Error"
          }
        });
	  }

}]);
