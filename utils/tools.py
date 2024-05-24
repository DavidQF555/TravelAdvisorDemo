import json
import requests
from datetime import datetime, timedelta
from pydantic.v1 import BaseModel, Field
from langchain.agents import tool
from dotenv import load_dotenv, find_dotenv
from .logger import logger
import os

class LocationInput(BaseModel):
    name: str = Field(description="name of the location")

def get_headers():
    _ = load_dotenv(find_dotenv())  # read local .env file
    return {
        'accept': 'application/json',
        'X-RapidAPI-Host': 'tripadvisor16.p.rapidapi.com',
        'X-RapidAPI-Key': os.getenv('RAPID_TRIP_ADVISOR_API_TOKEN')
    }

@tool(args_schema=LocationInput)
def get_restaurants(name: str) -> str:
    """Get the restraunts near the input location name"""

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchLocation"
    querystring = {"query": name}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the location with name: {name}. Response text: {response.text}"
    else:
        logger.debug(f"Requested successfully")
    data = response.json()['data']
    if(not data or len(data) == 0):
        return "Not found. Please try another question"
    location = data[0]["locationId"]

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchRestaurants"
    querystring = {"locationId": location}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the location with ID: {location}. Response text: {response.text}"
    else:
        logger.debug(f"Restraunts retrieved successfully")
    data = response.json()['data']['data']
    if not data or len(data) == 0:
        return "Not able to retrieve any restraunts. Please try another question"
    output = ""
    for val in data:
        output += f"Restraunt Name: {val['name']}\n"
        if len(val['establishmentTypeAndCuisineTags']) > 0:
            tags = ",".join(val['establishmentTypeAndCuisineTags'])
            output += f"Cuisine Types: {tags}\n"
        output += f"Average Rating: {val['averageRating']}\n"
        if val['hasMenu']:
            output += f"Menu URL: {val['menuUrl']}\n"
        output += val['currentOpenStatusText'] + "\n"
        output += "------------------------------------------------------\n"
    logger.debug(output)
    return output

@tool(args_schema=LocationInput)
def get_hotels(name: str) -> str:
    """Get the hotels near the input location name that have check in times today and checkout times in two days"""

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
    querystring = {"query": name}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the location with name: {name}. Response text: {response.text}"
    else:
        logger.debug(f"Requested successfully")
    data = response.json()['data']
    if(not data or len(data) == 0):
        return "Not found. Please try another question"
    location = data[0]["geoId"]
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {"geoId": location, 'checkIn': datetime.today().strftime('%Y-%m-%d'), 'checkOut': (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d') }
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the hotels at location: {val.name}. Response text: {response.text}"
    else:
        logger.debug(f"Hotels retrieved successfully")
    data = response.json()['data']['data']
    if not data or len(data) == 0:
        return "Not able to retrieve any hotels. Please try another question"
    output = ""
    for val in data:
        output += f"Hotel Name: {val['title']}\n"
        output += f"{val['primaryInfo']}\n"
        output += f"{val['secondaryInfo']}\n"
        output += f"Rated {val['bubbleRating']['rating']} by {val['bubbleRating']['count']} users\n"
        output += "------------------------------------------------------\n"
    logger.debug(output)
    return output
    

@tool(args_schema=LocationInput)
def get_airports(name: str) -> str:
    """Get the airports near the input location name"""
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport"
    headers = get_headers()
    response = requests.get(url, headers=headers, params={'query': name})
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the airports by: {name}. Response text: {response.text}"
    data = response.json()['data']
    if not data or len(data) == 0:
        return "Not able to retrieve any airports. Please try another question"
    output = ""
    for val in data:
        output += f"Short Name: {val['shortName']}\n"
        output += f"Full Name: {val['name']}\n"
        output += f"Airport Code: {val['airportCode']}\n"
        output += "------------------------------------------------------\n"
    logger.debug(output)
    return output