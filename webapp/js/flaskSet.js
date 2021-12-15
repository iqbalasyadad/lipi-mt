// FLASK FUNCTION //

function openCoordFile() {
    //pass
}

// function flaskGetSta() {
//     var url = "http://127.0.0.1:5000/getsta";            
//     var xhr = new XMLHttpRequest();
//     xhr.onerror = function() {
//         alert("Error");
//     }
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState == XMLHttpRequest.DONE) {
//             var staObj = JSON.parse(xhr.responseText);
//             // return JSON.parse(xhr.responseText);
//             // staObj = {sta1:{lat: lng:}, sta2:{lat: lng:}}
//             var staOverlay = L.featureGroup([]);
//             for (var key in staObj) {
//                 var staMarkerOptions = {radius: 5, staName: key};
//                 var staLatLng = [staObj[key]["lat"],staObj[key]["lng"]];
//                 var staMarker = L.circleMarker(staLatLng, staMarkerOptions);
//                 staMarker.bindPopup(key).openPopup();
//                 staOverlay.addLayer(staMarker);
//             }
//             myMap.map.addOverlayToMap(staOverlay, "station");
//         }
//     }
//     xhr.open("GET", url, true);
//     xhr.send();
// }

// async function flaskGetSta() {
//     let result = await makeRequest("GET", "http://127.0.0.1:5000/getsta");
//     let staObj = JSON.parse(result);
//     var staOverlay = L.featureGroup([]);
//     for (var key in staObj) {
//         var staMarkerOptions = {radius: 5, staName: key};
//         var staLatLng = [staObj[key]["lat"],staObj[key]["lng"]];
//         var staMarker = L.circleMarker(staLatLng, staMarkerOptions);
//         staMarker.bindPopup(key).openPopup();
//         staOverlay.addLayer(staMarker);
//     }
//     myMap.addOverlayToMap(staOverlay, "station");
// }

function makeRequest(method, url) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        xhr.send();
    });
}

