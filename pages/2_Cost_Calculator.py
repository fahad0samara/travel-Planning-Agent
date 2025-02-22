import streamlit as st
from tools.cost_calculator import CostCalculator

st.set_page_config(
    page_title="Cost Calculator - Travel Planning Agent",
    page_icon="💰",
    layout="wide"
)

st.title("Travel Cost Calculator")

# Initialize cost calculator
cost_calculator = CostCalculator()

# Display the calculator interface
cost_calculator.display_calculator()