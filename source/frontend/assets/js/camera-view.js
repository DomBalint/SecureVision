// On page load check for the camera Id in the url
const queryString = window.location.search;
// console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const camera_id = urlParams.get('id');
// console.log(camera_id);

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

async function get_image_info(da) {
    image_id = da[counter];
    counter++;
    if (counter === end - 1) {
        counter = 0;
    }
    // Get the latest image posted by required camera
    var data = {image_id: image_id};
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
        // console.log(response);
        // console.log(response.headers.get('Content-Type'));
        // console.log(response.headers.get('Date'));
        // console.log(response.status);
        // console.log(response.statusText);
        // console.log(response.type);
        // console.log(response.url);
        if (response.status === 200) {
            return response.json();
        } else {
            return null;
        }

    }).then(function (data) {
        if (data != null) {
            if (data['url'].startsWith("predictions"))
                url = data['url'].split("_")[0] + ".jpg";
            else
                url = "predictions/" + data['url'].split("/")[1];
            console.log(url)
            console.log(data['image_id']);
            //TODO: modify after the model connection to the database
            if (document.getElementById("image").src !== url)
                document.getElementById("image").src = url;
            image_id = data['image_id'];
            var detections = data['detections'];
            console.log(detections.length);
            draw_multiple_bb(detections);

            // if (detections.length !== 0)
            //     draw_multiple_bb(detections);
            // else
            //     clear_detections();

        }
    }).catch((error) => {
        console.error('Error:', error);
    });
}

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}


async function get_camera_images() {

    // Get the latest image posted by required camera
    var data = {camera_num: camera_id};
    var status = 0;
    var url = "http://localhost:5000/cameras";

    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)

    }).then(function (response) {

        // Log some information for debugging
        // console.log(response);
        // console.log(response.headers.get('Content-Type'));
        // console.log(response.headers.get('Date'));
        // console.log(response.status);
        // console.log(response.statusText);
        // console.log(response.type);
        // console.log(response.url);
        if (response.status === 200) {
            return response.json();
        } else {
            return null;
        }

    }).then(function (data) {
        if (data != null) {
            // for (let i = 0; i < data.length; i++) {
            //     get_image_info(data[i]);
            //     const sleep = (milliseconds) => {
            //         return new Promise(resolve => setTimeout(resolve,
            //             20000))
            //     }
            // }
            counter = 0;
            end = data.length;
            // image_id = data[0];
            setInterval(get_image_info, 2000, data);


        }

    }).catch((error) => {
        console.error('Error:', error);
    });
}


function delay(i) {
    setTimeout(get_image_info, 2000, i);
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
        // console.log(response);
        // console.log(response.headers.get('Content-Type'));
        // console.log(response.headers.get('Date'));
        // console.log(response.status);
        // console.log(response.statusText);
        // console.log(response.type);
        // console.log(response.url);

        if (response.status === 200) {
            return response.json();
        } else {
            return null;
        }

    }).then(function (data) {
        if (data != null) {
            alert("Feedback submitted successfully!");
            // console.log(data);
        }

    }).catch((error) => {
        console.error('Error:', error);
    });
}

function draw_image() {

}

window.onload = function () {
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    var img = document.getElementById("image");
    ctx.drawImage(img, 10, 10);
};

function draw_multiple_bb(detections) {

    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    var img = document.getElementById("image");
    new_width = 700;
    new_height = 500;
    ctx.canvas.width = new_width;
    ctx.canvas.height = new_height;

    img.onload = function () {
        ctx.drawImage(img, 10, 10, img.width, img.height, 0, 0, new_width, new_height);
        var canvas = document.getElementById('myCanvas');
        var context = canvas.getContext('2d');

        var boot_alert = document.getElementById("boot_alert");
        if (detections.length === 1) {
            boot_alert.innerText = "A threat has been detected!";
            boot_alert.classList = 'alert alert-danger';
        }
        else if (detections.length > 1) {
            boot_alert.innerText = "Multiple threats have been detected!";
            boot_alert.classList = 'alert alert-danger';
        } else {
            boot_alert.innerText = "All clear!";
            boot_alert.classList = 'alert alert-success';

        }

        var list = document.getElementById('threat_list');
        list.innerHTML = "";
        colors = ['red', 'blue', 'green', 'black', 'yellow'];
        for (var i = 0; i < detections.length; i++) {
            // console.log(detections[i]['threat']);
            // console.log(detections[i]['confidence'])

            var threat = detections[i]['threat'];
            var confidence = detections[i]['confidence'];
            var x = detections[i]['x'];
            var y = detections[i]['y'];
            var width = detections[i]['height'];
            var height = detections[i]['width'];

            // if (confidence < .5) {
            //     continue;
            // }
            context.beginPath();
            context.rect(x * new_width / img.width, y * new_height / img.height
                , width * new_width / img.width, height * new_height / img.height);
            // context.fillStyle = 'yellow';
            // context.fill();
            context.lineWidth = 3;
            context.strokeStyle = colors[i % colors.length];
            context.stroke();


            // inject the threats into the list with their confidence


            var entry = document.createElement('li');
            entry.classList = "list-group-item";
            entry.appendChild(document.createTextNode(threat + ":   " +
                parseFloat(confidence).toFixed(2) * 100 + "%"));
            list.appendChild(entry);
        }
    }

}


function draw_bb(x, y, width, height) {

    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    var img = document.getElementById("image");
    new_width = 300;
    new_height = 300;
    ctx.canvas.width = img.width;
    ctx.canvas.height = img.height;

    img.onload = function () {
        ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, new_width, new_height);
        // var canvas = document.getElementById('myCanvas');
        var context = c.getContext('2d');

        context.beginPath();
        context.rect(x * new_width / img.width, y * new_height / img.height
            , width * new_width / img.width, height * new_height / img.height);
        // context.fillStyle = 'yellow';
        // context.fill();
        context.lineWidth = 2;
        context.strokeStyle = 'red';
        context.stroke();
    }


}

get_camera_images();
// get_last_image();
// setInterval(get_last_image, 2000);