// Check if the user is already loged in
document.onload = function onload(){
	if (window.location.pathname != 'login.html'){
			if (!checkCookie('user_id')){
				window.location = "login.html";
			}
		}
}


// Request the user login api
var element = document.getElementById("login");
if (element != null)
element.onclick = function(event) {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var data = {username: username, password: password};
    Login(data);
}

async function Login(data) {
    var status = 0;
    var url="http://localhost:5000/user/login";
	
    const response = await fetch(url, {
    method: 'POST', 
    mode: 'cors', 
    headers: {
      'Content-Type': 'application/json',
    },
    redirect: 'follow', 
    body: JSON.stringify(data) 
			
  }).then(function(response) {
			
			// Logs for debugging remove later
      console.log(response);
      console.log(response.headers.get('Content-Type'));
      console.log(response.headers.get('Date'));
      console.log(response.status);
      console.log(response.statusText);
      console.log(response.type);
      console.log(response.url);
      if (response.status === 200){
          return response.json();
      }
        else{
            return null;
        }
      
}).then(function(data){
			if (data != null){
				console.log(data['id']);
				setCookie('user_id', data['id'], 1);
				window.location = "multi-camera.html";
			}
			else{
                swal("Error", "Incorrect credentials!", "error")
				// alert("Incorrect credentials!")
			}
}).catch((error) => {
      console.error('Error:', error);
});
}

// Set a new cookie
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// Fetch a pre-existing cookie
function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// Remove a cookie
function eraseCookie(cname) {
	if(checkCookie){
    	document.cookie = cname+'=; Max-Age=-99999999;';
	}
}

// check the existance of a cookie
function checkCookie(cname) {
  var user = getCookie(cname);
  if (user != "") {
   true; 
  }
	else{
		false;
	}
}


// Add the logout action
var logoutBTN = document.getElementById("logout");
logoutBTN.onclick = function(event) {
    logout();
}

function logout(cname){
    var user = getCookie(cname);
    if (user != "") {
        eraseCookie(cname);
		window.location = "login.html";
	}
	
}