# DestGPT - API Calling AI Agent

## Overview
Sample code for building an AI agent that calls Trip Advisor's API 
The structure and method can be generalized for other APIs. You can modify this code and build another agent that calls different APIs and achieve different effects.

Can ask questions about travel destinations, and the chatbot will retrieve and present relevant information from the the database.

**Note: this is a skeleton AI agent to serve the purpose of demo. It is by no means optimized or bug free. As a matter of fact, there are many areas where the agent can be improved.**

## Features

- **API Calling**: Uses the Trip Advisor's API to fetch detailed information about travel destinations.
- **Information Extraction**: Understands user queries and extracts relevant information.
- **Text Summarization**: Provides concise summaries of travel destination information.
- **Tagging**: Categorizes travel destinations based on user queries.
- **Interactive Interface**: Offers a conversational interface through Streamlit.

## Getting Started

### Prerequisites

- Python  3.x
- OpenAI api key
- Trip Advisor's API access through (Rapid API)[https://rapidapi.com/DataCrawler/api/tripadvisor16]
- Streamlit for the web application interface

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/DavidQF555/TravelAdvisorDemo.git
   ```
2. Navigate to the project directory:
   ```
   cd movieGPT
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   RAPID_TRIP_ADVISOR_API_TOKEN=your_rapid_api_key
   ```

### Running the Application

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Access the chatbot in your web browser at `http://localhost:8501`.
