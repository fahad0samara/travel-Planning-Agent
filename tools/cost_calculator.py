import streamlit as st
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TravelCost:
    category: str
    amount: float
    currency: str = 'USD'

class CostCalculator:
    def __init__(self):
        self.categories = {
            'Transportation': ['Flights', 'Local Transit', 'Car Rental'],
            'Accommodation': ['Hotels', 'Hostels', 'Vacation Rentals'],
            'Activities': ['Tours', 'Attractions', 'Entertainment'],
            'Food & Dining': ['Restaurants', 'Groceries', 'Snacks'],
            'Miscellaneous': ['Shopping', 'Insurance', 'Visa Fees']
        }
        self.city_costs = {
            'paris': {
                'budget': {
                    'accommodation': 70,  # Hostels or budget hotels
                    'food': 35,          # Street food, cafes, budget restaurants
                    'activities': 25,     # Basic museum passes, walking tours
                    'transport': 15       # Metro tickets, occasional bus
                },
                'moderate': {
                    'accommodation': 180,  # 3-star hotels or nice Airbnb
                    'food': 70,           # Mix of restaurants and cafes
                    'activities': 50,     # Museum passes, guided tours
                    'transport': 25       # Metro passes, occasional taxi
                },
                'luxury': {
                    'accommodation': 350,  # 4-5 star hotels
                    'food': 150,          # Fine dining, upscale restaurants
                    'activities': 100,     # Private tours, premium experiences
                    'transport': 50       # Taxis, private transfers
                }
            }
        }

    def display_calculator(self):
        """Display the travel cost calculator interface"""
        st.subheader('Travel Cost Calculator')
        
        total_cost = 0.0
        costs: List[TravelCost] = []

        with st.expander('Calculate Your Travel Costs', expanded=True):
            for category, subcategories in self.categories.items():
                st.write(f"### {category}")
                cols = st.columns(len(subcategories))
                
                for i, subcategory in enumerate(subcategories):
                    with cols[i]:
                        amount = st.number_input(
                            f"{subcategory}",
                            min_value=0.0,
                            value=0.0,
                            step=10.0,
                            key=f"cost_{category}_{subcategory}"
                        )
                        if amount > 0:
                            costs.append(TravelCost(subcategory, amount))
                            total_cost += amount

            st.markdown('---')
            st.markdown(f"### Total Estimated Cost: ${total_cost:,.2f}")

            if costs:
                st.write('### Cost Breakdown')
                data = {
                    'Category': [cost.category for cost in costs],
                    'Amount': [f"${cost.amount:,.2f}" for cost in costs]
                }
                st.dataframe(data, use_container_width=True)

    def get_budget_tips(self, total_cost: float) -> str:
        """Get budget-specific travel tips"""
        if total_cost < 1000:
            return "Budget-Friendly Tips:\n- Consider hostels or shared accommodations\n- Use public transportation\n- Cook some meals yourself\n- Look for free attractions and walking tours"
        elif total_cost < 3000:
            return "Mid-Range Budget Tips:\n- Mix hotels with budget accommodations\n- Balance dining out with self-catering\n- Look for city passes for attractions\n- Book transportation in advance"
        else:
            return "Luxury Budget Tips:\n- Consider travel insurance for high-value bookings\n- Look for package deals on premium experiences\n- Book direct flights for convenience\n- Research exclusive experiences and private tours"