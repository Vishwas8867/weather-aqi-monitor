# Weather AQI Monitor

## Overview

Weather AQI Monitor is a Python-based command-line application that retrieves and displays real-time weather information and air quality (AQI) data using the OpenWeather API. It shows temperature, humidity, wind speed, visibility, pollutant concentrations, and health recommendations with color-coded terminal output for better readability.

## Key Features

* Real-time weather metrics: temperature, feels-like temperature, humidity, pressure, wind speed, visibility, cloudiness
* Air Quality Index (AQI) with category and guidance
* Pollutant data: PM2.5, PM10, NO₂, O₃, CO, SO₂
* Basic weather-condition indicators
* Color-coded terminal display
* Error handling for invalid cities, API issues, and connection problems

## Requirements

* requests
* colorama

## Installation

pip install requests colorama

## Configuration

Get a free API key from:
[https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)

Set your key in the script:

API_KEY = "Your API Key"

## Usage

python weather.py
Enter a valid city name when prompted.

## Project Structure

weather-aqi-monitor/
├── weather.py \n
├── README.md \n
└── requirements.txt \n
