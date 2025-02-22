from typing import Any, Optional
from smolagents.tools import Tool
import requests
from datetime import datetime

class SafetyAdvisorTool(Tool):
    name = "safety_advisor"
    description = "Provides travel safety information, alerts, and advisories for destinations."
    inputs = {
        'destination': {'type': 'string', 'description': 'The destination country or city to get safety information for'},
        'travel_dates': {'type': 'string', 'description': 'Optional travel dates in YYYY-MM-DD format'}
    }
    output_type = "string"

    def __init__(self, api_key=None, *args, **kwargs):
        super().__init__()
        self.api_key = api_key or 'YOUR_TRAVEL_ADVISORY_API_KEY'
        self.base_url = 'https://www.travel-advisory.info/api'
        self.is_initialized = True

    def forward(self, destination: str, travel_dates: Optional[str] = None) -> str:
        try:
            # Make API request to get travel advisory data
            response = requests.get(f"{self.base_url}/all")
            if response.status_code != 200:
                return f"Error fetching travel advisory data: {response.status_code}"

            data = response.json()
            
            # Process and format the advisory information
            advisory_info = self._process_advisory_data(data, destination)
            
            # Add date-specific information if provided
            if travel_dates:
                advisory_info += f"\n\nTravel dates: {travel_dates}"
                advisory_info += self._get_seasonal_advice(destination, travel_dates)
            
            return advisory_info

        except Exception as e:
            return f"An error occurred while fetching travel safety information: {str(e)}"

    def _process_advisory_data(self, data: dict, destination: str) -> str:
        # Mock processing of advisory data
        safety_info = f"Travel Safety Information for {destination}:\n"
        safety_info += "\n1. General Safety Level: Moderate"
        safety_info += "\n2. Health Advisories:\n   - Recommended vaccinations up to date\n   - Travel insurance recommended"
        safety_info += "\n3. Security Concerns:\n   - Normal precautions advised\n   - Keep valuables secure"
        safety_info += "\n4. Emergency Contacts:\n   - Local Police: 911\n   - Tourist Police: +1-XXX-XXX-XXXX"
        
        return safety_info

    def _get_seasonal_advice(self, destination: str, travel_dates: str) -> str:
        try:
            travel_date = datetime.strptime(travel_dates, '%Y-%m-%d')
            month = travel_date.month
            
            seasonal_advice = "\n\nSeasonal Advice:"
            if 3 <= month <= 5:  # Spring
                seasonal_advice += "\n- Spring season: Pack for variable weather"
            elif 6 <= month <= 8:  # Summer
                seasonal_advice += "\n- Summer season: Prepare for high temperatures"
            elif 9 <= month <= 11:  # Fall
                seasonal_advice += "\n- Fall season: Pack layers for changing weather"
            else:  # Winter
                seasonal_advice += "\n- Winter season: Pack warm clothing"
                
            return seasonal_advice
        except:
            return "\n\nNote: Could not process seasonal advice for the provided dates."