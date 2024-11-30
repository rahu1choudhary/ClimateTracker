document.addEventListener('DOMContentLoaded', () => {
    const weatherStatus = document.getElementById('weather-status');
    const temperature = document.getElementById('temperature');
    const humidity = document.getElementById('humidity');
    const refreshButton = document.getElementById('refresh-weather');
    const historyContainer = document.getElementById('history-container');

    // Fetch weather data
    function fetchWeatherData() {
        setTimeout(() => {
            const weather = {
                status: ['Sunny', 'Rainy', 'Windy'][Math.floor(Math.random() * 3)], // Random status
                temp: Math.floor(Math.random() * 10 + 20), // Random temperature for demo
                humid: Math.floor(Math.random() * 20 + 50) // Random humidity for demo
            };
    
            // Update DOM
            weatherStatus.textContent = `Weather: ${weather.status}`;
            temperature.textContent = `Temperature: ${weather.temp}°C`;
            humidity.textContent = `Humidity: ${weather.humid}%`;
    
            // Add icon or alert based on weather conditions
            const weatherIcon = document.getElementById('weather-icon');
            weatherIcon.innerHTML = ''; // Clear previous icon or alert
    
            if (weather.status === 'Sunny') {
                weatherIcon.innerHTML = '<span class="sunny">☀️</span>';
            } else if (weather.status === 'Rainy') {
                weatherIcon.innerHTML = '<span class="rainy">🌧️</span>';
            } else if (weather.status === 'Windy') {
                weatherIcon.innerHTML = '<span class="windy">💨</span>';
            }
    
            if (weather.temp > 30) {
                weatherIcon.innerHTML += `<div class="alert">🔥 High temperature alert!</div>`;
            } else if (weather.humid > 70) {
                weatherIcon.innerHTML += `<div class="alert">💦 High humidity alert!</div>`;
            }
    
            // Add to history
            const now = new Date().toLocaleTimeString();
            const historyEntry = `At ${now} - ${weather.status}, ${weather.temp}°C, ${weather.humid}%`;
            const historyItem = document.createElement('p');
            historyItem.textContent = historyEntry;
            historyContainer.prepend(historyItem);
        }, 1000);
    }
    

    // Initial data load
    fetchWeatherData();
});
