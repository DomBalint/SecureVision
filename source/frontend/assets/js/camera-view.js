// On page load check for the camera Id in the url
const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const camera_id = urlParams.get('id');
get_data();
console.log(camera_id);

// Submit the a positive feedback using the like button
var like = document.getElementById("like");
like.onclick = function(event) {
    // var image_id = document.getElementById("image").value; // get the image id
    var data = {camera_num: camera_id, image_id: 1, feedback:1};
    Feedback(data);
}

var dislike = document.getElementById("dislike");
dislike.onclick = function(event) {
		 // var image_id = document.getElementById("image").value; // get the image id
    var data = {camera_num: camera_id, image_id: 1, feedback:0};
    Feedback(data);
}
async function get_data() {
		// Get the latest image posted by required camera
    var data = {camera_num: camera_id};
    var status = 0;
    var url="http://localhost:5000/image";
    const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    headers: {
      'Content-Type': 'application/json',
      //'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  }).then(function(response) {
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
						console.log(data['image_id']);
						console.log(data['url']);
						var detections  = data['detections'];
						if (detections != undefined){
								console.log(detections[0]['threat']);
								console.log(detections[0]['confidence']);
						// loop over the detecions and add them to the list
						// using injections or something like that
						// make the bootstrap alert visiable
						}
        }
}).catch((error) => {
      console.error('Error:', error);
});
}

// Call the Feedback api
async function Feedback(data) {
    var status = 0;
    var url="http://localhost:5000/image/feedback";
    const response = await fetch(url, {
    method: 'PUT', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    headers: {
      'Content-Type': 'application/json',
      //'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  }).then(function(response) {
		// Logs are for debugging
      console.log(response);
      console.log(response.headers.get('Content-Type'));
      console.log(response.headers.get('Date'));
      console.log(response.status);
      console.log(response.statusText);
      console.log(response.type);
      console.log(response.url);
			
      if (response.status === 201){
          return response.json();
      }
        else{
            return null;
        }
      
}).then(function(data){
        if (data != null){
			alert("Feedback submitted successfully!")
         	console.log(data);
			}
        
}).catch((error) => {
      console.error('Error:', error);
});
}
