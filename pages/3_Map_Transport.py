import streamlit as st
import folium
from streamlit_folium import folium_static
from tools.map_visualizer import MapVisualizer, Location
from tools.transport_guide import TransportGuideTool

st.title('Map & Transport Guide')

# Initialize tools
map_viz = MapVisualizer()
transport_guide = TransportGuideTool()

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader('Interactive Map')
    
    # Add location input fields
    origin = st.text_input('Starting Location', 'New York')
    destination = st.text_input('Destination', 'Boston')
    
    # Example coordinates (in real app, these would come from geocoding)
    start_loc = Location(origin, 40.7128, -74.0060)
    end_loc = Location(destination, 42.3601, -71.0589)
    
    # Create map centered on start location
    map_viz.add_location(start_loc)
    map_viz.add_location(end_loc)
    map_viz.add_route(start_loc, end_loc)
    
    # Display the map
    m = map_viz.visualize((start_loc.latitude, start_loc.longitude))
    folium_static(m)

with col2:
    st.subheader('Transport Options')
    
    # Transport type selector
    transport_type = st.selectbox(
        'Select Transport Type',
        ['All', 'Bus', 'Train', 'Taxi']
    )
    
    # Time input
    departure_time = st.time_input('Departure Time')
    
    # Get transport information
    if st.button('Show Transport Options'):
        transport_type_param = None if transport_type == 'All' else transport_type.lower()
        departure_time_str = departure_time.strftime('%H:%M')
        
        # Get and display transport information
        transport_info = transport_guide.forward(
            origin=origin,
            destination=destination,
            transport_type=transport_type_param,
            departure_time=departure_time_str
        )
        
        st.markdown(transport_info)