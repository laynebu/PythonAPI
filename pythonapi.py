import requests
from datetime import datetime
from dotenv import load_dotenv
import os


API_URL = "https://api.openweathermap.org/data/2.5/weather?appid={}&q={}&units={}"

load_dotenv()

def get_API_KEY():
    API_KEY = os.getenv('OWM_API_KEY')

    if not API_KEY:
        print('No API Key Found.')
        key = input('Please enter your OpenWeatherMap API Key: ')
        open('.env', 'w').write(f'OWM_API_KEY={key}\n')
        API_KEY = key
    return API_KEY

def get_weather(api_key, q, units):
    resp = requests.get(API_URL.format(api_key, q, units), timeout = 10)
    resp.raise_for_status() # 400 or 500 Errors
    weather = resp.json()

    if not weather:
        raise LookupError(f'No weather was found for this location')
    
    return weather


def main():
    api_key = get_API_KEY()
    while True:
        q = input('Please enter a Location (or quit to exit): ').lower()
        if  q == 'quit':
            break
        units = input('Please enter preferred units("Metric" / "Imperial"): ').lower()
        try:
            weather = get_weather(api_key, q, units)
        except requests.exceptions.RequestException as e:
            print(f'A Network/HTTP error occurred: {e}')
            print('Try Again. Ensure everything is typed correctly')
            continue
        except LookupError as e:
            print(e)
            print('Try Again. Ensure everything is typed correctly')
            continue
        except ValueError as e:
            print('The server response did not match valid JSON')
            print('Try Again. Ensure everything is typed correctly')
            continue
        else:
            if units == 'imperial':
                tempunit = 'F'
                windunit = 'mph'
            if units == 'metric':
                tempunit = 'C'
                windunit = 'kmh'
            location = weather.get("name", {})
            temp = weather.get("main", {}).get("temp")
            humidity = weather.get("main", {}).get("humidity")
            wind = weather.get("wind", {}).get("speed")
            sunrise = weather.get("sys", {}).get("sunrise")
            sunset = weather.get("sys", {}).get("sunset")
            sunrise_converted = datetime.fromtimestamp(sunrise)
            sunset_converted = datetime.fromtimestamp(sunset)
            print(f'Weather for {location}:')
            print(f'The Temperature is {temp} degrees {tempunit}')
            print(f'The Humidity is {humidity}%')
            print(f'Windspeed is {wind} {windunit}')
            print("Sunrise:", sunrise_converted.strftime("%I:%M %p"))
            print("Sunset:", sunset_converted.strftime("%I:%M %p"))
if __name__ == "__main__":
    main()