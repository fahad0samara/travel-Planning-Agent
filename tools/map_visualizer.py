import folium
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Location:
    name: str
    latitude: float
    longitude: float
    description: str = ''
    category: str = 'destination'

class MapVisualizer:
    def __init__(self):
        self.markers = []
        self.routes = []

    def create_map(self, center: Tuple[float, float] = (0, 0), zoom: int = 2) -> folium.Map:
        """Create a new map centered at the specified coordinates.
        
        Args:
            center (Tuple[float, float]): Center coordinates (latitude, longitude)
            zoom (int): Initial zoom level
        
        Returns:
            folium.Map: The created map object
        """
        return folium.Map(location=center, zoom_start=zoom)

    def add_location(self, location: Location) -> None:
        """Add a location marker to the map.
        
        Args:
            location (Location): Location details
        """
        self.markers.append(location)

    def add_route(self, start: Location, end: Location, mode: str = 'travel') -> None:
        """Add a route between two locations.
        
        Args:
            start (Location): Starting location
            end (Location): Ending location
            mode (str): Travel mode (e.g., 'driving', 'walking', 'flying')
        """
        self.routes.append({
            'start': start,
            'end': end,
            'mode': mode
        })

    def visualize(self, center: Tuple[float, float] = None) -> folium.Map:
        """Create and return the visualization map with all markers and routes.
        
        Args:
            center (Tuple[float, float], optional): Center coordinates
        
        Returns:
            folium.Map: The complete map with all visualizations
        """
        # If no center is provided, use the first marker or default
        if not center and self.markers:
            center = (self.markers[0].latitude, self.markers[0].longitude)
        elif not center:
            center = (0, 0)

        # Create the map
        m = self.create_map(center=center)

        # Add markers
        for location in self.markers:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=folium.Popup(
                    f"<b>{location.name}</b><br>{location.description}",
                    max_width=300
                ),
                icon=folium.Icon(color=self._get_marker_color(location.category))
            ).add_to(m)

        # Add routes
        for route in self.routes:
            coordinates = [
                [route['start'].latitude, route['start'].longitude],
                [route['end'].latitude, route['end'].longitude]
            ]
            folium.PolyLine(
                coordinates,
                weight=2,
                color=self._get_route_color(route['mode']),
                opacity=0.8
            ).add_to(m)

        return m

    def _get_marker_color(self, category: str) -> str:
        """Get the marker color based on the location category."""
        colors = {
            'destination': 'red',
            'hotel': 'blue',
            'restaurant': 'green',
            'attraction': 'purple',
            'event': 'orange'
        }
        return colors.get(category.lower(), 'gray')

    def _get_route_color(self, mode: str) -> str:
        """Get the route color based on the travel mode."""
        colors = {
            'driving': 'blue',
            'walking': 'green',
            'flying': 'red',
            'transit': 'orange'
        }
        return colors.get(mode.lower(), 'gray')

    def save_map(self, map_obj: folium.Map, filepath: str) -> None:
        """Save the map to an HTML file.
        
        Args:
            map_obj (folium.Map): The map object to save
            filepath (str): Path where to save the HTML file
        """
        map_obj.save(filepath)