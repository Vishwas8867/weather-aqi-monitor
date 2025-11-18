# Weather AQI Monitor

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Requests](https://img.shields.io/badge/Requests-HTTP%20Client-green)
![Colorama](https://img.shields.io/badge/Colorama-CLI%20Colors-yellow)
![OpenWeather](https://img.shields.io/badge/API-OpenWeather-orange)
![AQI](https://img.shields.io/badge/AQI-Monitoring-red)

A lightweight command-line tool that fetches **real-time weather** and **air quality (AQI)** for any city using OpenWeather APIs.

It provides:
- Temperature in °C and °F  
- Weather description + emoji  
- Humidity, wind, pressure, visibility, cloudiness  
- Sunrise & sunset  
- AQI level with color-coded alert  
- Pollutant breakdown (PM2.5, PM10, NO₂, O₃, CO, SO₂)  
- Health advice based on AQI & pollutant levels  

---

## 🚀 Features

- Fetches current weather (`/weather` API)  
- Fetches air pollution & AQI (`/air_pollution` API)  
- Colourised output using **Colorama**  
- Automatic pollutant risk detection  
- Clean CLI display with emojis  
- Graceful error handling (404, timeout, invalid key, etc.)

---

## 📦 Requirements

- Python **3.8+**
- OpenWeather API key  
  Get one free: https://openweathermap.org/api

---

## ⚙️ Installation

```bash
git clone https://github.com/Vishwas8867/weather-aqi-monitor/
cd weather-aqi-monitor

python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.\\.venv\\Scripts\\activate    # Windows

pip install -r requirements.txt
