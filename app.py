from smolagents import CodeAgent, DuckDuckGoSearchTool, load_tool, tool, LiteLLMModel, TransformersModel
import datetime
import requests
import pytz
import yaml
import os
import google.generativeai as genai
from tools.final_answer import FinalAnswerTool
from tools.visit_webpage import VisitWebpageTool
from tools.web_search import DuckDuckGoSearchTool
from streamlit_app import StreamlitUI
from smolagents.agents import MultiStepAgent
import json

# Load agent configuration
with open('agent.json', 'r') as f:
    agent_config = json.load(f)

# Configure Gemini API

# Initialize tools
visit_webpage = VisitWebpageTool()
web_search = DuckDuckGoSearchTool()
final_answer = FinalAnswerTool()


# Initialize the model with proper configuration


model = LiteLLMModel(
  model_id="gemini/gemini-2.0-flash-exp",
  max_tokens=2096,
  temperature=0.6,
  api_key="AIzaSyDq7dxX4H8bhWokg9NRqY7j999Pw47sQjc"
)

# Initialize the agent
agent = MultiStepAgent(
    model=model,
    tools=[visit_webpage, web_search, final_answer],
    max_steps=6
)

# Initialize and run the Streamlit UI
ui = StreamlitUI(agent)
ui.run()

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

if __name__ == "__main__":
    try:
        ui = StreamlitUI(agent)
        ui.run()
    except Exception as e:
        print(f"Error launching StreamlitUI: {str(e)}")
