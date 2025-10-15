import requests
import json
from operator import itemgetter

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

def get_temp(location):
	
	# Retrive location from OpenMeteo with its API

	url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"

	a = requests.get(url)
	b = a.json()

	# print(b)
	# b is as follow
	'''
	{'results': 
	[{'id': 1816670, 
	'name': 'Beijing',
	'latitude': 39.9075, 
	'longitude': 116.39723, 
	'elevation': 49.0, 
	'feature_code': 'PPLC', 
	'country_code': 'CN', 
	'admin1_id': 2038349, 
	'admin2_id': 11876380, 
	'timezone': 'Asia/Shanghai', 
	'population': 18960744, 
	'country_id': 1814991, 
	'country': 'China', 
	'admin1': 'Beijing', 
	'admin2': 'Beijing'}], 
	'generationtime_ms': 0.32007694}

	'''

	# Get Data Needed

	data = b['results'][0]
	keys = ['latitude', 'longitude']
	params_needed = itemgetter(*keys)(data)

	'''
	params_needed is (latitude, longitude)

	'''
	# print(params_needed)

	# Get Max and Min Temperature with OpenMeteo Weather API

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)	
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": params_needed[0],
		"longitude": params_needed[1],
    	"forecast_days": 1,
		"daily": ["temperature_2m_max", "temperature_2m_min"]}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]

	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left")}

	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min

	max = daily_data["temperature_2m_max"][0]
	min = daily_data["temperature_2m_min"][0]

	temperature = round(((max + min) / 2))

	return temperature

