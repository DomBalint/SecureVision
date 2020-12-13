async function get_cameras() {
	
    var status = 0;
    var url="http://localhost:8432/cameras";
    const response = await fetch(url, {
    method: 'GET', 
    mode: 'cors', 
    headers: {
      'Content-Type': 'application/json',
    },
    
  }).then(function(response) {
			
			// Log some information for debugging
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
					for (var i=0; i < data.length; i++){
						console.log(data[i]['cam_id']);
						console.log(data[i]['is_running']);
						get_image(data[i]['cam_id']);
					}
        }
}).catch((error) => {
      console.error('Error:', error);
});
}
async function get_image(camera_id) {
	
		// Get the latest image posted by required camera
    var data = {camera_num: camera_id};
    var status = 0;
    var url="http://localhost:8432/image";
	
    const response = await fetch(url, {
    method: 'POST', 
    mode: 'cors', 
    headers: {
      'Content-Type': 'application/json',
    },
    redirect: 'follow', 
    body: JSON.stringify(data) 
			
  }).then(function(response) {
			
			// Log some information for debugging
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
						for (var i=1; i < 5; i++){
							// TODO: uncomment to work with the model
							// document.getElementById("Image" +i).src = data['url'];
					}
						}
}).catch((error) => {
      console.error('Error:', error);
});
}

get_cameras();




// setInterval(get_cameras, 2000);