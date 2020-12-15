// On page load check for the camera Id in the url
const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const camera_id = urlParams.get('id');
console.log(camera_id);

// Submit the a positive feedback using the like button
var like = document.getElementById("like");
like.onclick = function (event) {
    var data = {camera_num: camera_id, image_id: image_id, feedback: 1};
    Feedback(data);
}

var dislike = document.getElementById("dislike");
dislike.onclick = function (event) {
    var data = {camera_num: camera_id, image_id: image_id, feedback: 0};
    Feedback(data);
}

async function get_last_image() {

    // Get the latest image posted by required camera
    var data = {camera_num: camera_id};
    var status = 0;
    var url = "http://localhost:5000/image";

    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)

    }).then(function (response) {

        // Log some information for debugging
        console.log(response);
        console.log(response.headers.get('Content-Type'));
        console.log(response.headers.get('Date'));
        console.log(response.status);
        console.log(response.statusText);
        console.log(response.type);
        console.log(response.url);
        if (response.status === 200) {
            return response.json();
        } else {
            return null;
        }

    }).then(function (data) {
        if (data != null) {
            console.log(data['image_id']);
            console.log(data['url']);
            //TODO: modify after the model connection to the database
            document.getElementById("image").src = data['url'];
            image_id = data['image_id'];
            var detections = data['detections'];
            if (detections != undefined) {
                for (var i = 0; i < detections.length; i++) {
                    console.log(detections[i]['threat']);
                    console.log(detections[i]['confidence']);
                }
                // TODO: inject the detectoins to the list
            }
        }
    }).catch((error) => {
        console.error('Error:', error);
    });
}

// Call the Feedback api
async function Feedback(data) {
    var status = 0;
    var url = "http://localhost:5000/image/feedback";

    const response = await fetch(url, {
        method: 'PUT',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        body: JSON.stringify(data)

    }).then(function (response) {

        // Log some information for debugging
        console.log(response);
        console.log(response.headers.get('Content-Type'));
        console.log(response.headers.get('Date'));
        console.log(response.status);
        console.log(response.statusText);
        console.log(response.type);
        console.log(response.url);

        if (response.status === 200) {
            return response.json();
        } else {
            return null;
        }

    }).then(function (data) {
        if (data != null) {
            alert("Feedback submitted successfully!");
            console.log(data);
        }

    }).catch((error) => {
        console.error('Error:', error);
    });
}


// get_data();
setInterval(get_last_image, 2000);