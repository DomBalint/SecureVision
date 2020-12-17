async function get_cameras() {

    var status = 0;
    var url = "http://localhost:5000/cameras";
    const response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
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
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]['cam_id']);
                console.log(data[i]['is_running']);
                if (data[i]['is_running'])
                    get_camera_images(data[i]['cam_id']);
                // break;
            }
        }
    }).catch((error) => {
        console.error('Error:', error);
    });
}


async function get_image_info(da, cam_num) {
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
            if (data['url'].startsWith("predictions"))
                url = data['url'].split("_")[0] + ".jpg";
            else
                url = "predictions/" + data['url'].split("/")[1];
            console.log(data['image_id']);
            console.log(url);
            //TODO: modify after the model connection to the database
            if (document.getElementById("Image" + cam_num).src !== url)
                document.getElementById("Image" + cam_num).src = url;
            image_id = data['image_id'];
            var detections = data['detections'];
            // if (detections !== undefined) {
            //     for (var i = 0; i < detections.length; i++) {
            //         console.log(detections[i]['threat']);
            //         console.log(detections[i]['confidence']);
            //     }
            //     // TODO: inject the detectoins to the list
            // }
            // sleep(2000);
            // draw_bb(174, 354, 162, 102);
            // if (detections.length > 0)
            // draw_multiple_bb(detections);
        }
    }).catch((error) => {
        console.error('Error:', error);
    });
}

async function get_camera_images(camera_id) {

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
            setInterval(get_image_info, 2000, data, camera_id);


        }

    }).catch((error) => {
        console.error('Error:', error);
    });
}

//
// async function get_image(camera_id) {
//
//     // Get the latest image posted by required camera
//     var data = {camera_num: camera_id};
//     var status = 0;
//     var url = "http://localhost:5000/image";
//
//     const response = await fetch(url, {
//         method: 'POST',
//         mode: 'cors',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         redirect: 'follow',
//         body: JSON.stringify(data)
//
//     }).then(function (response) {
//
//         // Log some information for debugging
//         console.log(response);
//         console.log(response.headers.get('Content-Type'));
//         console.log(response.headers.get('Date'));
//         console.log(response.status);
//         console.log(response.statusText);
//         console.log(response.type);
//         console.log(response.url);
//         if (response.status === 200) {
//             return response.json();
//         } else {
//             return null;
//         }
//
//     }).then(function (data) {
//         if (data != null) {
//
//             url = data['url'].substring(0, 18) + ".jpg";
//             console.log(data['image_id']);
//             console.log(url);
//             // for (var i = 1; i < 5; i++) {
//                 document.getElementById("Image" +camera_id).src = url;
//             // }
//         }
//     }).catch((error) => {
//         console.error('Error:', error);
//     });
// }

get_cameras();


// setInterval(get_cameras, 2000);