# Travel Planning Agent

A comprehensive travel planning assistant powered by AI that helps users plan their trips, calculate costs, check weather, and find transportation options.

## Features

- **Interactive Chat Interface**: Ask questions about travel destinations, accommodations, and attractions
- **Weather Service**: Check weather conditions for your destination
- **Cost Calculator**: Estimate and plan your travel budget
- **Transportation Guide**: Get information about local transport options and schedules
- **Map Visualization**: View locations and routes on interactive maps

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Set up your environment variables in `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
python -m streamlit run app.py
```

2. Navigate to the different pages:
   - Main Chat Interface: Ask travel-related questions
   - Weather: Check destination weather forecasts
   - Cost Calculator: Plan your travel budget
   - Map & Transport: View routes and transportation options

## Backend Integration

### API Endpoints

#### Weather Service
```
GET /api/weather
Query Parameters:
- city (required): Name of the city
- days (optional): Number of forecast days (default: 5)

Response:
{
    "current": {
        "temperature": float,
        "conditions": string,
        "humidity": integer
    },
    "forecast": [...]
}
```

#### Cost Calculator
```
POST /api/calculate-costs
Body:
{
    "destination": string,
    "duration": integer,
    "travelers": integer,
    "preferences": {
        "accommodation_type": string,
        "transportation_mode": string
    }
}

Response:
{
    "total_cost": float,
    "breakdown": {
        "accommodation": float,
        "transportation": float,
        "activities": float,
        "food": float
    }
}
```

#### Transport Guide
```
GET /api/transport
Query Parameters:
- origin (required): Starting location
- destination (required): End location
- mode (optional): Transport mode preference

Response:
{
    "routes": [
        {
            "mode": string,
            "duration": string,
            "cost": float,
            "steps": [...]
        }
    ]
}
```

### Authentication

The API uses JWT (JSON Web Token) authentication:

1. Obtain access token:
```
POST /api/auth/token
Body:
{
    "username": string,
    "password": string
}

Response:
{
    "access_token": string,
    "token_type": "bearer",
    "expires_in": integer
}
```

2. Use the token in subsequent requests:
```
Authorization: Bearer <access_token>
```

### Data Models

#### User
```python
class User:
    id: int
    username: str
    email: str
    preferences: Dict
```

#### Trip
```python
class Trip:
    id: int
    user_id: int
    destination: str
    start_date: datetime
    end_date: datetime
    budget: float
    itinerary: List[Activity]
```

#### Activity
```python
class Activity:
    id: int
    trip_id: int
    name: str
    date: datetime
    location: str
    cost: float
```

### Error Handling

The API uses standard HTTP status codes and returns error responses in the following format:
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": object (optional)
    }
}
```

## Configuration

The agent's behavior and capabilities can be configured in `agent.json`:
- Model settings (temperature, max tokens)
- Available tools and their configurations
- System prompts and expertise areas
- Response format structure

## Dependencies

- streamlit: Web application framework
- smolagents: Agent toolkit
- requests: HTTP client
- duckduckgo_search: Web search capability
- pandas: Data manipulation
- litellm: LLM interface
- streamlit-folium: Map visualization
- folium: Interactive maps

## Project Structure

```
├── .streamlit/          # Streamlit configuration
├── pages/               # Additional web pages
├── tools/               # Agent tools and utilities
│   ├── cost_calculator.py
│   ├── transport_guide.py
│   ├── weather_service.py
│   └── web_search.py
├── app.py               # Main application entry
├── streamlit_app.py     # Streamlit UI implementation
├── agent.json           # Agent configuration
└── requirements.txt     # Project dependencies
```

## Features in Detail

### Weather Service
Check current weather conditions and forecasts for any destination.

### Cost Calculator
Plan your budget with estimates for:
- Transportation
- Accommodation
- Activities
- Food and dining

### Transportation Guide
Get information about:
- Local transport options
- Route planning
- Schedule information
- Fare estimates

### Map Visualization
- Interactive maps
- Route visualization
- Points of interest

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.