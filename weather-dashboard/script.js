document.addEventListener('DOMContentLoaded', () => {
    const weatherStatus = document.getElementById('weather-status');
    const temperature = document.getElementById('temperature');
    const humidity = document.getElementById('humidity');
    const weatherIcon = document.getElementById('weather-icon');
    const cityInput = document.getElementById('city-input');
    const fetchWeatherButton = document.getElementById('fetch-weather');
    const refreshButton = document.getElementById('refresh-weather');
    const historyContainer = document.getElementById('history-container');

    // Function to fetch weather data from the server
    async function fetchWeatherData(city) {
        try {
            const response = await fetch(`http://localhost:5000/weather/${city}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch weather data: ${response.statusText}`);
            }
            const data = await response.json();
            
            // Update the DOM with fetched data
            weatherStatus.textContent = `Weather: ${data.cloud ? data.cloud : 'Clear'}`;
            temperature.textContent = `Temperature: ${data.temperature_c}°C`;
            humidity.textContent = `Humidity: ${data.humidity}%`;

            // Update the icon based on the weather status
            weatherIcon.innerHTML = '';
            if (data.cloud === 'Clear') {
                weatherIcon.innerHTML = '<span class="sunny">☀️</span>';
            } else if (data.cloud.includes('Rain')) {
                weatherIcon.innerHTML = '<span class="rainy">🌧️</span>';
            } else {
                weatherIcon.innerHTML = '<span class="windy">💨</span>';
            }

            // Add history
            const now = new Date().toLocaleTimeString();
            const historyEntry = `At ${now} - ${data.cloud}, ${data.temperature_c}°C, ${data.humidity}%`;
            const historyItem = document.createElement('p');
            historyItem.textContent = historyEntry;
            historyContainer.prepend(historyItem);

        } catch (error) {
            console.error('Error fetching weather data:', error);
            weatherStatus.textContent = 'Error fetching data';
        }
    }

    // Event listener for the "Get Weather" button
    fetchWeatherButton.addEventListener('click', () => {
        const city = cityInput.value.trim();
        if (city) {
            fetchWeatherData(city);
        } else {
            alert('Please enter a city name');
        }
    });

    // Event listener for the "Refresh" button
    refreshButton.addEventListener('click', () => {
        const city = cityInput.value.trim();
        if (city) {
            fetchWeatherData(city);
        } else {
            alert('Please enter a city name to refresh the weather');
        }
    });
});
