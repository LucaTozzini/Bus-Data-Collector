import requests

openweatherUrl = 'https://api.openweathermap.org/data/2.5/weather'
openweatherKey = 'key'

def openWeatherRequest(lat, lon):
    # A GET request to the API
    url = '{}?lat={}&lon={}&appid={}'.format(openweatherUrl, lat, lon, openweatherKey)
    response = requests.get(url)

    # Print the response
    response_json = response.json()
    return response_json