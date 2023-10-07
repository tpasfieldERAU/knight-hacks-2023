const map = L.map('map').setView([51.505, -0.09], 13);

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
