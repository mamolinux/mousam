import requests
current_weather_data = None
forecast_weather_data = None

def get_weather_data():
    return current_weather_data,forecast_weather_data

def set_weather_data(current,forecast):
    global current_weather_data, forecast_weather_data
    current_weather_data = current
    forecast_weather_data = forecast

def check_internet_connection():
    url = "http://www.google.com"
    timeout = 10  # Set the timeout value in seconds
    response_text = ""
    has_active_internet = False
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print("Internet connection is active.")
            has_active_internet = True
            return has_active_internet, response_text

    except requests.RequestException as e:
        print("Internet connection is not available.")
        print(str(e))
        response_text = "No internet connection!"
        has_active_internet = True
        return has_active_internet, response_text
    except requests.Timeout:
        print("Request timed out.")
        response_text = "Connection timeout!"
        return has_active_internet, response_text
