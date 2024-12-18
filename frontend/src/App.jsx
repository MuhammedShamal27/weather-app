import React, { useState } from "react";
import "./App.css"; 

function App() {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Function to fetch weather data
  const fetchWeatherData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/weather");
      if (!response.ok) throw new Error("Failed to fetch weather data");

      const data = await response.json();
      setWeatherData(data);
    } catch (err) {
      setError(err.message || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Weather Report</h1>

      {/* Button to fetch data */}
      {!weatherData && !loading && (
        <button className="fetch-button" onClick={fetchWeatherData}>
          Fetch Weather Data
        </button>
      )}

      {/* Loading state */}
      {loading && <p className="loading">Loading...</p>}

      {/* Error state */}
      {error && <p className="error">{error}</p>}

      {/* Weather Data Table */}
      {weatherData && (
        <table className="weather-table">
          <thead>
            <tr>
              <th>Place</th>
              <th>Time</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {weatherData.map((item, index) => (
              <tr key={index}>
                <td>{item.place}</td>
                <td>{item.date}</td>
                <td>{item.temperature}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
