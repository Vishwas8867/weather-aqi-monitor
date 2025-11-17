import os
import requests
from datetime import datetime

try:
    from colorama import init, Fore, Style
except ImportError:
    raise SystemExit("Install colorama first: pip install colorama")

init(autoreset=True)

# API key 
API_KEY = "Your API Key"

def kelvin_to_celsius(k): return k - 273.15
def kelvin_to_fahrenheit(k): return (k * 9/5) - 459.67

def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232: return "⛈"
    if 300 <= weather_id <= 321: return "🌦"
    if 500 <= weather_id <= 531: return "🌧"
    if 600 <= weather_id <= 622: return "❄"
    if 701 <= weather_id <= 741: return "🌫"
    if weather_id == 762: return "🌋"
    if weather_id == 771: return "💨"
    if weather_id == 781: return "🌪"
    if weather_id == 800: return "☀"
    if 801 <= weather_id <= 804: return "☁"
    return ""

def fetch_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY}
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    return r.json()

def fetch_aqi(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    return r.json()

def aqi_label_and_advice(aqi_value):
    mapping = {
        1: ("Good", "😃",
             ["Air quality is satisfactory.", "No action needed. Enjoy outdoor activities."]),
        2: ("Fair", "🙂",
             ["Air quality is acceptable.", "If sensitive, reduce prolonged outdoor exertion."]),
        3: ("Moderate", "😐",
             ["Sensitive individuals: limit prolonged outdoor exertion.", "Consider mask if you have lung/cardiac conditions."]),
        4: ("Poor", "😷",
             ["Sensitive groups avoid prolonged outdoor exertion.", "Consider a high-quality mask (N95/FFP2)."]),
        5: ("Very Poor", "🤢",
             ["Avoid outdoor exertion; stay indoors if possible.", "Use air purifiers and high-quality masks if needed."])
    }
    return mapping.get(aqi_value, ("Unknown","",["AQI data unavailable."]))

def pollutant_tips(components):
    tips = []
    pm25 = components.get("pm2_5")
    pm10 = components.get("pm10")
    o3 = components.get("o3")
    no2 = components.get("no2")
    co = components.get("co")
    so2 = components.get("so2")

    if pm25 is not None and pm25 > 35:
        tips.append(f"PM2.5 = {pm25} μg/m³ — high. Reduce outdoor activities; use mask/air purifier.")
    if pm10 is not None and pm10 > 50:
        tips.append(f"PM10 = {pm10} μg/m³ — elevated. Avoid dusty outdoor work.")
    if o3 is not None and o3 > 120:
        tips.append(f"O₃ = {o3} μg/m³ — ozone high. Avoid vigorous outdoor exercise (afternoons).")
    if no2 is not None and no2 > 100:
        tips.append(f"NO₂ = {no2} μg/m³ — elevated. Limit time near traffic.")
    if co is not None and co > 10000:
        tips.append(f"CO = {co} μg/m³ — high. Seek fresh air and ventilation.")
    if so2 is not None and so2 > 100:
        tips.append(f"SO₂ = {so2} μg/m³ — elevated. Asthmatics should be cautious.")
    return tips

def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%I:%M %p")

def color_for_aqi(aqi):
    # Return Fore color for AQI (1..5)
    if aqi == 1: return Fore.GREEN
    if aqi == 2: return Fore.CYAN
    if aqi == 3: return Fore.YELLOW
    if aqi == 4: return Fore.MAGENTA
    if aqi == 5: return Fore.RED
    return Fore.WHITE

def display_weather_and_aqi(weather_data, aqi_data):
    temp_k = weather_data["main"]["temp"]
    temp_c = kelvin_to_celsius(temp_k)
    temp_f = kelvin_to_fahrenheit(temp_k)
    feels_c = kelvin_to_celsius(weather_data["main"].get("feels_like", temp_k))
    wind = weather_data.get("wind", {}).get("speed", "N/A")
    pressure = weather_data["main"].get("pressure", "N/A")
    humidity = weather_data["main"].get("humidity", "N/A")
    visibility = weather_data.get("visibility", 0) / 1000
    clouds = weather_data.get("clouds", {}).get("all", "N/A")
    sunrise = format_time(weather_data["sys"]["sunrise"])
    sunset = format_time(weather_data["sys"]["sunset"])

    wid = weather_data["weather"][0]["id"]
    desc = weather_data["weather"][0]["description"].title()
    city_name = f"{weather_data.get('name')}, {weather_data.get('sys', {}).get('country')}"
    emoji = get_weather_emoji(wid)

    # Header
    print(Style.BRIGHT + "="*48)
    print(color_text(f"📍 Location: {city_name}", Fore.CYAN))
    print(color_text(f"{emoji}  {desc}", Fore.YELLOW))
    print(color_text(f"🌡 Temperature: {temp_c:.1f}°C / {temp_f:.1f}°F   (Feels: {feels_c:.1f}°C)", Fore.GREEN))
    print(f"💧 Humidity: {humidity}%    🌬 Wind: {wind} m/s    🔵 Pressure: {pressure} hPa")
    print(f"👁 Visibility: {visibility:.1f} km    ☁ Cloudiness: {clouds}%")
    print(f"🌅 Sunrise: {sunrise}    🌇 Sunset: {sunset}")
    print("="*48 + Style.RESET_ALL)

    # AQI block
    try:
        first = aqi_data.get("list", [])[0]
        aqi_val = first["main"]["aqi"]
        label, emot, advice_list = aqi_label_and_advice(aqi_val)
        comps = first.get("components", {})

        aqi_color = color_for_aqi(aqi_val)
        aqi_line = color_text(f"AQI (OpenWeather): {aqi_val} — {label} {emot}", aqi_color + Style.BRIGHT)
        print("\n" + aqi_line)

        # Pollutants table
        print(color_text("Key pollutants (μg/m³):", Fore.WHITE + Style.BRIGHT))
        for p in ("pm2_5","pm10","no2","o3","co","so2"):
            val = comps.get(p, "N/A")
            # highlight high pollutant values in yellow/red
            display_val = str(val)
            if isinstance(val, (int, float)):
                if p == "pm2_5" and val > 35:
                    display_val = color_text(display_val, Fore.RED)
                elif p == "pm10" and val > 50:
                    display_val = color_text(display_val, Fore.RED)
                elif p in ("no2","o3","so2") and val > 100:
                    display_val = color_text(display_val, Fore.MAGENTA)
            print(f"  {p:6}: {display_val}")
        # general advice
        print("\n" + color_text("Health advice:", Fore.YELLOW + Style.BRIGHT))
        for adv in advice_list:
            print(" -", adv)
        p_tips = pollutant_tips(comps)
        if p_tips:
            print(color_text("\nAdditional pollutant-specific tips:", Fore.MAGENTA + Style.BRIGHT))
            for t in p_tips:
                print(" -", t)
        print()
    except Exception:
        print(color_text("\nAQI: Data unavailable.\n", Fore.RED))

def display_error(msg):
    print(color_text("\nERROR: " + str(msg) + "\n", Fore.RED + Style.BRIGHT))

def main():
    city = input("Enter city name: ").strip()
    if not city:
        print("No city entered. Exiting.")
        return

    try:
        weather = fetch_weather(city)
        cod = int(weather.get("cod", 0))
        if cod != 200:
            display_error(weather.get("message", "Failed to get weather"))
            return

        coord = weather.get("coord", {})
        lat = coord.get("lat"); lon = coord.get("lon")
        aqi = None
        if lat is not None and lon is not None:
            try:
                aqi = fetch_aqi(lat, lon)
            except requests.exceptions.RequestException:
                aqi = None

        display_weather_and_aqi(weather, aqi or {})
    except requests.exceptions.HTTPError as http_err:
        status = getattr(http_err.response, "status_code", None)
        errors = {
            400: "Bad request — check city name.",
            401: "Unauthorized — invalid API key.",
            403: "Forbidden — access denied.",
            404: "City not found.",
            500: "Server error — try again later."
        }
        display_error(errors.get(status, f"HTTP error: {http_err}"))
    except requests.exceptions.ConnectionError:
        display_error("Connection error — check internet.")
    except requests.exceptions.Timeout:
        display_error("Request timed out.")
    except requests.exceptions.RequestException as e:
        display_error(f"Request failed: {e}")

if __name__ == "__main__":
    main()