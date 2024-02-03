from datetime import datetime
from .backendWeather import Weather
from .backendAirPollution import AirPollution
from .Models import *

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gio


current_weather_data = None
hourly_forecast_data = None
daily_forecast_data = None
air_apllution_data = None


def get_cords():
    settings = Gio.Settings(schema_id="io.github.amit9838.weather")
    selected_city_ = settings.get_string('selected-city')   
    return [float(x) for x in selected_city_.split(",")]

def fetch_current_weather():
    global current_weather_data
    # Get current weather data from api
    obj = Weather()
    current_weather_data = obj._get_current_weather(*get_cords())

    # create object of current weather data
    current_weather_data = CurrentWeather(current_weather_data)

    # Add level strings for diffrent attributes
    current_weather_data.relativehumidity_2m["level_str"] = classify_humidity_level(current_weather_data.relativehumidity_2m.get("data"))
    current_weather_data.windspeed_10m["level_str"] = classify_wind_speed_level(current_weather_data.windspeed_10m.get("data"))
    current_weather_data.surface_pressure["level_str"] = classify_presssure_level(current_weather_data.surface_pressure.get("data"))

    return current_weather_data

def fetch_hourly_forecast():
    global hourly_forecast_data
    # Get current weather data from api
    obj = Weather()
    hourly_forecast_data = obj._get_hourly_forecast(*get_cords())
    # create object of hourly forecast data
    hourly_forecast_data = HourlyWeather(hourly_forecast_data)
    set_uv_index()

    return hourly_forecast_data

def fetch_daily_forecast():
    global daily_forecast_data

    # Get current weather data from api
    obj = Weather()
    daily_forecast_data = obj._get_daily_forecast(*get_cords())

    # create object of daily forecast data
    daily_forecast_data = DailyWeather(daily_forecast_data)

    return daily_forecast_data

def fetch_current_air_pollution():
    global air_apllution_data
    obj = AirPollution()
    air_apllution_data = obj._get_current_air_pollution(*get_cords())
    if air_apllution_data is not None:
        air_apllution_data["level"] = classify_aqi(air_apllution_data["current"]["us_aqi"])
    return air_apllution_data


def classify_aqi(aqi_value):
    if aqi_value >= 0 and aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Satisfactory"
    elif aqi_value <= 200:
        return "Moderate"
    elif aqi_value <= 300:
        return "Poor"
    elif aqi_value <= 400:
        return "Very Poor"
    elif aqi_value <= 500:
        return "Severe"
    else:
        return "Hazardous"
    
    
def set_uv_index():
    date_time = [d_t for d_t in hourly_forecast_data.time["data"] if (int(datetime.fromtimestamp(d_t).strftime(r"%d")) == datetime.today().date().day)]
    date_time = [d_t for d_t in date_time if int(datetime.fromtimestamp(d_t).strftime(r"%H")) == datetime.now().hour]
    date_time = date_time[0]
    
    uv_index = 0
    for i,item in enumerate(hourly_forecast_data.time["data"]):
        if item == date_time:
            uv_index = {
                        "data": hourly_forecast_data.uv_index["data"][i],
                        "level_str": classify_uv_index(hourly_forecast_data.uv_index["data"][i])
                        }
            
            
    current_weather_data.uv_index = uv_index
    return uv_index


# ========= Classify diffrent attributes of current weather ==========

def classify_uv_index(uv_index):
    if uv_index <= 2:
        return "Low"
    elif uv_index <= 5:
        return "Moderate"
    elif uv_index <= 7:
        return "High"
    elif uv_index <= 10:
        return "Very High"
    else:
        return "Extreme"


def classify_humidity_level(uv_index):
    if uv_index < 50:
        return "Low"
    elif uv_index <= 80:
        return "Moderate"
    else:
        return "High"
    

def classify_presssure_level(pressure):
    if pressure < 940:
        return "Low"
    elif pressure <= 1010:
        return "Normal"
    else:
        return "High"
    

def classify_wind_speed_level(wind_speed):
    if wind_speed <= 1:
        return "Calm"
    elif wind_speed <= 25:
        return "Light"
    elif wind_speed <= 40:
        return "Moderate"
    elif wind_speed <= 60:
        return "Strong"
    else:
        return "Extreme"
