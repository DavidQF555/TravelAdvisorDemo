import requests
import json
from pydantic.v1 import BaseModel, Field
from langchain.agents import tool
from dotenv import load_dotenv, find_dotenv
import os

class LocationInput(BaseModel):
    name: str = Field(description="name of the location")

class HotelInput(LocationInput):
    checkIn_year: int = Field(description="year for checking in")
    checkIn_month: int = Field(description="month for checking in")
    checkIn_day: int = Field(description="day for checking in")
    checkOut_year: int = Field(description="year for checking out")
    checkOut_month: int = Field(description="month for checking out")
    checkOut_day: int = Field(description="day for checking out")

class FlightInput(BaseModel):
    sourceAirport: str = Field(description="airport code of source airport")
    destAirport: str = Field(description="airport code of destination airport")
    year: int = Field(description="year of the flight")
    month: int = Field(description="month of the flight")
    day: int = Field(description="day of the flight")
    round_trip: bool = Field(description="whether the flight is round trip")
    num_adults: int = Field(description="number of adults")
    num_seniors: int = Field(description="number of seniors")
    service_class: str = Field(description="class of flight (ECONOMY, PREMIUM_ECONOMY, BUSINESS, or FIRST)")
    

def get_headers():
    _ = load_dotenv(find_dotenv())  # read local .env file
    return {
        'accept': 'application/json',
        'X-RapidAPI-Host': 'tripadvisor16.p.rapidapi.com',
        'X-RapidAPI-Key': os.getenv('RAPID_TRIP_ADVISOR_API_TOKEN')
    }

from utils.logger import logger

foundMovie = {}

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
    data = response.json()
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
    data = response.json()['data']
    if not data or len(data) == 0:
        return "Not able to retrieve any restraunts. Please try another question"
    output = ""
    for val in data:
        output += f"Restraunt Name: {val['name']}\n"
        output += val['currentOpenStatusText'] + "\n"
        output += "------------------------------------------------------\n"
    logger.debug(output)
    return output

@tool(args_schema=HotelInput)
def get_hotels(name: str, checkIn_year: int, checkIn_month: int, checkIn_day: int, checkOut_year: int, checkOut_month: int, checkOut_day: int) -> str:
    """Get the hotels near the input location name"""

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
    data = response.json()
    if(not data or len(data) == 0):
        return "Not found. Please try another question"
    location = data[0]["documentId"]
    
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {"geoId": location, "checkIn": f"{checkIn_year}-{checkIn_month}-{checkIn_day}", "checkOut": f"{checkOut_year}-{checkOut_month}-{checkOut_day}"}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the hotels at location: {name}. Response text: {response.text}"
    else:
        logger.debug(f"Hotels retrieved successfully")
    data = response.json()['data']
    if not data or len(data) == 0:
        return "Not able to retrieve any hotels. Please try another question"
    output = ""
    for val in data:
        output += f"Hotel Name: {val['title']}\n"
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
    print(response.json())
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the airports by: {name}. Response text: {response.text}"
    data = response.json()
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
    
@tool(args_schema=FlightInput)
def get_flights(sourceAirport: str, destAirport: str, year: int, month: int, day: int, round_trip: bool, num_adults: int, num_seniors: int, service_class: str) -> str:
    """Get the flights with the input source airport and destination airport codes"""

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights"

    querystring = {
        "sourceAirportCode": sourceAirport,
        "destinationAirportCode": destAirport,
        "date": f"{year}-{month}-{day}",
        "itineraryType": "ROUND_TRIP" if round_trip else "ONE_WAY",
        "sortOrder": "ML_BEST_VALUE",
        "numAdults": num_adults,
        "numSeniors": num_seniors,
        "classOfService": service_class
    }
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve any flights from {sourceAirport} to {destAirport}. Response text: {response.text}"
    data = response.json()['flights']
    if not data or len(data) == 0:
        return f"Not able to retrieve any flights. Please try another question"
    output = ""
    for val in data:
        for i, segment in enumerate(val['segments'], 1):
            output += f"Segment {i}:\n"
            for j, leg in enumerate(segment['legs'], 1):
                output += f"Leg {j}:\n"
                output += f"Origin Airport Code: {leg['originStationCode']}\n"
                output += f"Destination Airport Code: {leg['destinationStationCode']}\n"
                output += f"Departure Date-Time: {leg['departureDateTime']}\n"
                output += f"Arrival Date-Time: {leg['arrivalDateTime']}\n"
        output += "Purchase Links:\n"
        for link in val['purchaseLinks']:
            output += f"Price: {link['totalPrice']} {link['currency']} Purchase Link: {link['url']}\n"
        output += "------------------------------------------------------\n"
    logger.debug(output)
    return output