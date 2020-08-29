#!/usr/bin/env python3

# cli for getting current temperature from a given location
# script defaults to Longmont, CO, but you can specify any zip or country of your choosing

# couple main things this script does:
# 1. Sets up the argument parser for the CLI
# 2. Grabs API key from env var
# 3. Verifies that there is an API key
# 4. Constructs url to hit with interpolation from arg parser
# 5. Makes request and stores is as a variable
# 6. Checks the status code from API
# 7. Converts response from API into a python dict object
# 8. Returns formatted results

import os
import requests
import sys
import json

from argparse import ArgumentParser

# setup cli arguments
parser = ArgumentParser(description='Get the current weather information for your zip code')
parser.add_argument('zip', nargs='?', default=80503, help='zip/postal code to get weather for')
parser.add_argument('--country', default='us', help='country zip/postal belongs to, default is "us"')

args = parser.parse_args()

# set the API key from environment variable
api_key = os.getenv('OWM_API_KEY')

# check to see if API key is present
if not api_key:
    print("Error: no API key provided")
    sys.exit(1)

# make API call
def api_call():
    # define URL to hit
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={args.zip},{args.country}&appid={api_key}&units=imperial"

    # construct GET request
    res = requests.get(url)
    
    if res.status_code != 200:
        print(f"Error talking to weather provider: {res.status_code}")
        sys.exit(2)

    # serialize json to a string
    # data = json.dumps(res.json(), indent=2)

    # deserialize to a python dictionary object
    # parse = json.loads(data)

    # this way way easier than above; grabs raw text/json output, then deserializes it into a dict object
    parse = json.loads(res.text)

    location_name = parse["name"]
    actual_temp = parse["main"]['temp']
    relative_temp = parse["main"]['feels_like']
    high = parse["main"]['temp_max']
    low = parse["main"]['temp_min']

    print(f'**Current temperature conditions for {location_name}**\n Actual temp: {actual_temp}F\n Feels like: {relative_temp}\n High: {high}F\n Low: {low}F')

if __name__ == "__main__":
    location = str(args.zip)

    if location.isdigit():
        api_call()
    else:
        print(f"'{location}' not accepted, location must be in zip format: 80305, 90210, etc.")
        sys.exit(3)