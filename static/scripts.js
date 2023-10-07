const map = L.map('map').setView([45.0, -35.0], 3);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

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

            // Add new markers
            data.forEach(item => {
                const { lat, lon, name } = item;
                const marker = L.marker([lat, lon]).addTo(map);
                marker.bindPopup(name);
            });
        })
        .catch(error => {
            console.error('Error updating coordinates:', error);
        });
}

// Attach the updateMarkers function to the button click event
document.getElementById('updateButton').addEventListener('click', updateMarkers);

// Load initial markers from Flask
fetch('/get_coordinates', { method: 'GET' })
    .then(response => response.json())
    .then(data => {
        // Add initial markers
        data.forEach(item => {
            const { lat, lon, name } = item;
            const marker = L.marker([lat, lon]).addTo(map);
            marker.bindPopup(name);
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
            deviceMarker.bindPopup("Your Location").openPopup();

            // Pan the map to the device's location
            // map.setView([latitude, longitude], 13);
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
    // document.getElementById('latitude').value = '';
}

document.getElementById('airportForm').addEventListener('submit', handleFormSubmission);

// Call the updateDeviceLocation function to initially set the device's location
updateDeviceLocation();

// Set an interval to periodically update the device's location
setInterval(updateDeviceLocation, 300000); // Update every 5 minutes.