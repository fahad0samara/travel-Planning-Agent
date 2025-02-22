from typing import Any, Optional
from smolagents.tools import Tool
import requests
from datetime import datetime

class TransportGuideTool(Tool):
    name = "transport_guide"
    description = "Provides local transportation information, route planning, and fare estimates."
    inputs = {
        'origin': {'type': 'string', 'description': 'Starting location'},
        'destination': {'type': 'string', 'description': 'Destination location'},
        'transport_type': {'type': 'string', 'description': 'Type of transport (bus, train, taxi, etc.)', 'optional': True, 'nullable': True},
        'departure_time': {'type': 'string', 'description': 'Optional departure time in HH:MM format', 'optional': True, 'nullable': True}
    }
    output_type = "string"

    def __init__(self, api_key=None, *args, **kwargs):
        super().__init__()
        self.api_key = api_key or 'YOUR_TRANSPORT_API_KEY'
        self.is_initialized = True

    def forward(self, origin: str, destination: str, transport_type: Optional[str] = None,
                departure_time: Optional[str] = None) -> str:
        try:
            # Mock transport data processing
            transport_info = self._get_transport_options(origin, destination, transport_type)
            if departure_time:
                transport_info += self._get_schedule_info(departure_time)
            return transport_info

        except Exception as e:
            return f"An error occurred while fetching transportation information: {str(e)}"

    def _get_transport_options(self, origin: str, destination: str, transport_type: Optional[str]) -> str:
        info = f"\nTransportation Options from {origin} to {destination}:\n"
        
        # Mock different transportation options
        options = {
            'bus': {'route': 'Route 101', 'duration': '45 mins', 'fare': '$2.50'},
            'train': {'route': 'Blue Line', 'duration': '30 mins', 'fare': '$3.00'},
            'taxi': {'route': 'Direct', 'duration': '25 mins', 'fare': '$20.00'}
        }

        if transport_type and transport_type.lower() in options:
            option = options[transport_type.lower()]
            info += f"\n{transport_type.title()}:"
            info += f"\n- Route: {option['route']}"
            info += f"\n- Estimated Duration: {option['duration']}"
            info += f"\n- Estimated Fare: {option['fare']}"
        else:
            for t_type, details in options.items():
                info += f"\n{t_type.title()}:"
                info += f"\n- Route: {details['route']}"
                info += f"\n- Estimated Duration: {details['duration']}"
                info += f"\n- Estimated Fare: {details['fare']}"
                info += "\n"

        return info

    def _get_schedule_info(self, departure_time: str) -> str:
        try:
            time = datetime.strptime(departure_time, '%H:%M')
            schedule_info = f"\nSchedule Information for {departure_time}:"
            schedule_info += "\n- Next available departure: " + time.strftime('%H:%M')
            schedule_info += "\n- Service frequency: Every 15 minutes"
            schedule_info += "\n- Peak hours: 07:00-09:00 and 16:00-18:00"
            return schedule_info
        except:
            return "\n\nNote: Could not process schedule information for the provided time."