const map = L.map('map').setView([29.1802, -81.0598], 11);
let current_planes = [];
let select = null;

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var planeIcon = L.icon({
    iconUrl: '/static/plane.png',

    iconSize:     [32, 32], // size of the icon
    iconAnchor:   [16, 16], // point of the icon which will correspond to marker's location
    popupAnchor:  [16, 0] // point from which the popup should open relative to the iconAnchor
});


// Function to update markers on the map
function updateMarkers() {
    fetch('/update_coordinates', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Remove existing markers
            map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });

            current_planes = [];
            // Add new markers
            data.forEach(item => {
                const { reg, mod, lat, lon, alt, vspeed, hspeed, head, arv, dep } = item;
                const marker = L.marker([lat, lon], {icon: planeIcon}).addTo(map);
                marker.bindPopup(reg);

                marker.on('click', function () {
                    // Handle the marker click event
                    select = marker.getPopup().getContent();
                    updateTable(select);
                });

                const plane = {reg:reg, mod:mod, lat:lat, lon:lon, alt:alt, vspeed:vspeed, hspeed:hspeed, head:head, arv:arv, dep:dep}
                current_planes.push(plane)
            });
        })
        .catch(error => {
            console.error('Error updating coordinates:', error);
        });
    if (select != null) {
        updateTable(select);
    }
}


// Load initial markers from Flask
fetch('/get_coordinates', { method: 'GET' })
    .then(response => response.json())
    .then(data => {
        // Add initial markers
        data.forEach(item => {
            const { reg, mod, lat, lon, alt, vspeed, hspeed, head, arv, dep} = item;
            const marker = L.marker([lat, lon], {icon: planeIcon}).addTo(map);
            marker.bindPopup(reg);

            marker.on('click', function () {
                // Handle the marker click event
                select = marker.getPopup().getContent();
                updateTable(select);
            });

            const plane = {reg:reg, mod:mod, lat:lat, lon:lon, alt:alt, vspeed:vspeed, hspeed:hspeed, head:head, arv:arv, dep:dep}
            current_planes.push(plane)
        });
    })
    .catch(error => {
        console.error('Error loading initial coordinates:', error);
    });



function updateDeviceLocation() {
    // Check if geolocation is available in the browser
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(position => {
            const { latitude, longitude } = position.coords;

            // Remove existing location marker
            if (typeof deviceMarker !== "undefined") {
                map.removeLayer(deviceMarker);
            }

            // Add a marker for the device's location
            deviceMarker = L.marker([latitude, longitude]).addTo(map);

            // Pan the map to the device's location
            map.setView([latitude, longitude], 13);
        }, error => {
            console.error("Error getting device location:", error.message);
        });
    } else {
        console.error("Geolocation is not available in this browser.");
    }
}

function handleFormSubmission(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the latitude and longitude values from the form
    const icao = document.getElementById('icao').value;

    // Send the icao code to flask
    fetch('/set_airport', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(icao),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server, which may include updated marker data
        const {lat, lon} = data;
        map.setView([lat, lon], 12);
    })
    .catch(error => {
        console.error('Error setting airport:', error);
    });

    // Clear the form fields
    document.getElementById('icao').value = '';

    fetch('/get_coordinates', { method: 'GET' })
    .then(response => response.json())
    .then(data => {
        // Add initial markers
        data.forEach(item => {
            const { reg, mod, lat, lon, alt, vspeed, hspeed, head, arv, dep} = item;
            const marker = L.marker([lat, lon], {icon: planeIcon}).addTo(map);
            marker.bindPopup(reg);

            marker.on('click', function () {
                // Handle the marker click event
                select = marker.getPopup().getContent();
                updateTable(select);
            });

            const plane = {reg:reg, mod:mod, lat:lat, lon:lon, alt:alt, vspeed:vspeed, hspeed:hspeed, head:head, arv:arv, dep:dep}
            current_planes.push(plane)
        });
    })
    .catch(error => {
        console.error('Error loading initial coordinates:', error);
    });

}

function updateTable(reg) {
    current_planes.forEach(plane => {
        if(plane.reg === reg) {
            dispPlane = plane
        }
    });
    document.getElementById('bigreg').innerHTML = dispPlane["reg"];
    document.getElementById('reg').innerHTML = dispPlane["reg"];
    document.getElementById('mod').innerHTML = dispPlane["mod"];
    document.getElementById('alt').innerHTML = dispPlane["alt"];
    document.getElementById('hspeed').innerHTML = dispPlane["hspeed"];
    document.getElementById('vspeed').innerHTML = dispPlane["vspeed"];
    document.getElementById('head').innerHTML = dispPlane["head"];
    document.getElementById('dep').innerHTML = dispPlane["dep"];
    document.getElementById('arv').innerHTML = dispPlane["arv"];
}
document.getElementById('airportForm').addEventListener('submit', handleFormSubmission);

setInterval(updateMarkers, 15000)