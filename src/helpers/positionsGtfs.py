import csv
import datetime
import requests
from weather import *

def positionsGtfs():
    response = requests.get('http://localhost/ai/trainingData')
    data = response.json()

    for bus in data:
        try:
            weatherData = openWeatherRequest(bus['lat'], bus['lng'])

            expected_arrival = datetime.datetime.fromtimestamp(bus['expected_arrival']).strftime("%H:%M:%S")
            expected_hour = int(expected_arrival.split(':')[0])
            expected_minute = int(expected_arrival.split(':')[1])

            scheduled_hour = int(bus['scheduled_arrival'].split(':')[0])
            if scheduled_hour > 23 and expected_hour < 5:
                expected_arrival += 24
            scheduled_min = int(bus['scheduled_arrival'].split(':')[1])

            bus['punctualityDifference'] = ((expected_hour*60) + expected_minute) - ((scheduled_hour*60) + scheduled_min)

            bus['late'] = bus['punctualityDifference'] > 0
            bus['early'] = bus['punctualityDifference'] < 0
            bus['on_time'] = bus['punctualityDifference'] == 0

            bus['weatherDescription'] = weatherData['weather'][0]['description']
            bus['temperature'] = weatherData['main']['temp']
            bus['visibility'] = weatherData['visibility']

            with open("../data/trainingData.csv", "a", newline="") as csvfile:
                fieldnames = list(bus.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(bus)
        except:
            print('error caught')

positionsGtfs()