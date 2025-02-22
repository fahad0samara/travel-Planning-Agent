import streamlit as st
import os
import re
import shutil
from typing import Optional
from smolagents.agent_types import AgentAudio, AgentImage, AgentText, handle_agent_output_types
from smolagents.agents import ActionStep, MultiStepAgent
from smolagents.memory import MemoryStep

class StreamlitUI:
    def __init__(self, agent: MultiStepAgent, file_upload_folder: str | None = None):
        self.agent = agent
        self.file_upload_folder = file_upload_folder
        if self.file_upload_folder is not None:
            if not os.path.exists(file_upload_folder):
                os.mkdir(file_upload_folder)

    def apply_custom_css(self):
        st.markdown("""
        <style>
        /* Global styles */
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #1a1a1a;
            line-height: 1.7;
            background: #f8fafc;
        }

        /* Chat container */
        .main-content {
            max-width: 100%;
            margin: 0 auto;
            padding: 1rem;
            padding-bottom: 9rem;
        }
        @media (min-width: 768px) {
            .main-content {
                max-width: min(92%, 1100px);
                padding: 2rem 1rem;
            }
        }

        /* Chat messages */
        .chat-message {
            padding: 1.25rem 1.75rem;
            border-radius: 1.2rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: flex-start;
            gap: 1.25rem;
            animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
            max-width: 85%;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .chat-message:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 12px -2px rgba(0, 0, 0, 0.12), 0 4px 6px -2px rgba(0, 0, 0, 0.08);
        }

        .chat-message.user {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 0.4rem;
        }

        .chat-message.assistant {
            background: white;
            border: 1px solid #e2e8f0;
            margin-right: auto;
            border-bottom-left-radius: 0.4rem;
        }

        /* Avatar */
        .chat-message .avatar {
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-size: 1.3rem;
            flex-shrink: 0;
            background: #f1f5f9;
            border: 2.5px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }

        .chat-message.user .avatar {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.5);
            order: 2;
        }

        .chat-message:hover .avatar {
            transform: scale(1.1) rotate(5deg);
        }

        /* Message content */
        .chat-message .message {
            flex-grow: 1;
            overflow-wrap: break-word;
            word-wrap: break-word;
            hyphens: auto;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        /* Input box */
        .stTextInput {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1.25rem;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(12px);
            border-top: 1px solid #e2e8f0;
            z-index: 100;
            box-shadow: 0 -8px 16px -4px rgba(0, 0, 0, 0.1);
        }

        .stTextInput > div {
            max-width: min(92%, 1100px);
            margin: 0 auto;
        }

        .stTextInput input {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem 1.25rem;
            font-size: 1.05rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .stTextInput input:focus {
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        /* Sidebar improvements */
        .css-1d391kg, .css-1544g2n {
            padding: 2.5rem 1.5rem;
            background: white;
            border-right: 1px solid #e2e8f0;
        }

        /* Example buttons */
        .stButton button {
            width: 100%;
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            border: 1px solid #e2e8f0;
            background: white;
            color: #1a1a1a;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            margin-bottom: 0.5rem;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .stButton button:hover {
            background: #f8fafc;
            border-color: #4f46e5;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-content {
                padding: 1rem 0.75rem;
                padding-bottom: 8rem;
            }

            .chat-message {
                padding: 1rem 1.25rem;
                margin-bottom: 1.5rem;
                max-width: 92%;
            }

            .chat-message .avatar {
                width: 34px;
                height: 34px;
                font-size: 1.1rem;
            }

            .chat-message .message {
                font-size: 1rem;
            }

            .stTextInput {
                padding: 1rem;
            }

            .stTextInput input {
                padding: 0.6rem 1rem;
                font-size: 1rem;
            }
        }

        /* Loading animation */
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }

        .loading-indicator {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            margin: 1rem 0;
            color: #4f46e5;
            font-size: 1.2rem;
            animation: pulse 1.5s ease-in-out infinite;
        }

        /* Enhanced chat message styling */
        .chat-message .message pre {
            background: rgba(0, 0, 0, 0.05);
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin: 0.5rem 0;
        }

        .chat-message.assistant .message pre {
            background: rgba(79, 70, 229, 0.1);
        }

        .chat-message .message p {
            margin: 0.5rem 0;
        }

        .chat-message .message ul,
        .chat-message .message ol {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
        }

        /* Improved scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(79, 70, 229, 0.3);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(79, 70, 229, 0.5);
        }

        .chat-message:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 12px -2px rgba(0, 0, 0, 0.12), 0 4px 6px -2px rgba(0, 0, 0, 0.08);
        }

        .chat-message.user {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 0.4rem;
        }

        .chat-message.assistant {
            background: white;
            border: 1px solid #e2e8f0;
            margin-right: auto;
            border-bottom-left-radius: 0.4rem;
        }

        /* Avatar */
        .chat-message .avatar {
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-size: 1.3rem;
            flex-shrink: 0;
            background: #f1f5f9;
            border: 2.5px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }

        .chat-message.user .avatar {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.5);
            order: 2;
        }

        .chat-message:hover .avatar {
            transform: scale(1.1) rotate(5deg);
        }

        /* Message content */
        .chat-message .message {
            flex-grow: 1;
            overflow-wrap: break-word;
            word-wrap: break-word;
            hyphens: auto;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        /* Input box */
        .stTextInput {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1.25rem;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(12px);
            border-top: 1px solid #e2e8f0;
            z-index: 100;
            box-shadow: 0 -8px 16px -4px rgba(0, 0, 0, 0.1);
        }

        .stTextInput > div {
            max-width: min(92%, 1100px);
            margin: 0 auto;
        }

        .stTextInput input {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem 1.25rem;
            font-size: 1.05rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .stTextInput input:focus {
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        /* Sidebar improvements */
        .css-1d391kg, .css-1544g2n {
            padding: 2.5rem 1.5rem;
            background: white;
            border-right: 1px solid #e2e8f0;
        }

        /* Example buttons */
        .stButton button {
            width: 100%;
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            border: 1px solid #e2e8f0;
            background: white;
            color: #1a1a1a;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            margin-bottom: 0.5rem;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .stButton button:hover {
            background: #f8fafc;
            border-color: #4f46e5;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-content {
                padding: 1rem 0.75rem;
                padding-bottom: 8rem;
            }

            .chat-message {
                padding: 1rem 1.25rem;
                margin-bottom: 1.5rem;
                max-width: 92%;
            }

            .chat-message .avatar {
                width: 34px;
                height: 34px;
                font-size: 1.1rem;
            }

            .chat-message .message {
                font-size: 1rem;
            }

            .stTextInput {
                padding: 1rem;
            }

            .stTextInput input {
                padding: 0.6rem 1rem;
                font-size: 1rem;
            }
        }

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            body {
                background: #0f172a;
                color: #f1f5f9;
            }

            .chat-message.assistant {
                background: #1e293b;
                border-color: #334155;
            }

            .stTextInput {
                background: rgba(15, 23, 42, 0.98);
                border-top-color: #334155;
            }

            .stTextInput input {
                background: #1e293b;
                border-color: #334155;
                color: #f1f5f9;
            }

            .stTextInput input:focus {
                border-color: #6366f1;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
            }

            .stButton button {
                background: #1e293b;
                border-color: #334155;
                color: #f1f5f9;
            }

            .stButton button:hover {
                background: #334155;
                border-color: #6366f1;
            }
        }

        /* Improved mobile responsiveness */
        @media (max-width: 480px) {
            .chat-message {
                max-width: 95%;
                padding: 0.75rem 1rem;
                margin-bottom: 1rem;
            }

            .chat-message .avatar {
                width: 30px;
                height: 30px;
                font-size: 1rem;
            }

            .chat-message .message {
                font-size: 0.95rem;
            }

            .stTextInput {
                padding: 0.75rem;
            }

            .stTextInput input {
                padding: 0.5rem 0.75rem;
                font-size: 0.95rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)

    def process_agent_response(self, task: str, reset_agent_memory: bool = False):
        total_input_tokens = 0
        total_output_tokens = 0
        messages = []
        final_response = ""

        for step_log in self.agent.run(task, stream=True, reset=reset_agent_memory):
            if hasattr(self.agent.model, "last_input_token_count") and \
               self.agent.model.last_input_token_count is not None and \
               self.agent.model.last_output_token_count is not None:
                total_input_tokens += self.agent.model.last_input_token_count
                total_output_tokens += self.agent.model.last_output_token_count

        # Handle final answer
        final_answer = handle_agent_output_types(step_log)
        if isinstance(final_answer, AgentText):
            final_response = final_answer.to_string()
            st.write(final_response)
        elif isinstance(final_answer, AgentImage):
            final_response = final_answer.to_string()
            st.image(final_response)
        elif isinstance(final_answer, AgentAudio):
            final_response = final_answer.to_string()
            st.audio(final_response)
        else:
            final_response = str(final_answer)
            st.write(final_response)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": final_response})

    def display_message(self, role, content):
        if role == "user":
            avatar = "👤"
            style_class = "user"
        else:
            avatar = "🤖"
            style_class = "assistant"

        message_html = f"""
        <div class="chat-message {style_class}">
            <div class="avatar">{avatar}</div>
            <div class="message">{content}</div>
        </div>
        """
        st.markdown(message_html, unsafe_allow_html=True)

    def run(self):
        self.apply_custom_css()
        st.title("Travel Planning Assistant")
        st.markdown("""
        <div class='main-content'>
            <p>Welcome to your personal travel planning assistant! Ask me anything about travel destinations, 
            accommodations, transportation, or local attractions.</p>
        </div>
        """, unsafe_allow_html=True)

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("What would you like to know about your travel destination?", key="chat_input"):
            st.session_state["messages"].append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            with st.chat_message("assistant"):
                response = self.agent.run(prompt)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.write(response)

        st.rerun()

    def display_message(self, role, content):
        if role == "user":
            avatar = "👤"
            style_class = "user"
        else:
            avatar = "🤖"
            style_class = "assistant"

        message_html = f"""
        <div class="chat-message {style_class}">
            <div class="avatar">{avatar}</div>
            <div class="message">{content}</div>
        </div>
        """
        st.markdown(message_html, unsafe_allow_html=True)

    def run(self):
        st.set_page_config(
            page_title="Travel Planning Agent",
            layout="wide"
        )
        
        self.apply_custom_css()

        # Main chat area
        st.markdown('<div class="main-content">', unsafe_allow_html=True)

        # Example questions
        col1, col2 = st.columns([3, 1])
        with col2:
            st.subheader("Example Questions")
            examples = [
                "What are the best beaches to visit in Bali, Indonesia?",
                "How much should I budget for a week in Paris?",
                "What's the best time to see the Northern Lights in Iceland?",
                "What cultural etiquette should I know before visiting Dubai?",
                "Recommend a 3-day itinerary for Barcelona, Spain",
                "Which vaccinations do I need for a trip to Thailand?"
            ]
            
            for i, example in enumerate(examples):
                if st.button(example, key=f"example_{i}", use_container_width=True):
                    st.session_state.user_input = example
                    st.session_state.submit_clicked = True
                    # Add message to chat history
                    st.session_state.messages.append({"role": "user", "content": example})
                    self.display_message("user", example)
                    # Process the response
                    with st.spinner("🤔 Thinking..."):
                        self.process_agent_response(example)
                    st.rerun()

        with col1:
            # Initialize session state for chat history
            if 'messages' not in st.session_state:
                st.session_state.messages = []

            # Display chat history
            for message in st.session_state.messages:
                self.display_message(message["role"], message["content"])

            # Chat input and send button in a row
            col_input, col_button = st.columns([6, 1])
            with col_input:
                # Initialize the session state for input if not exists
                if "user_input" not in st.session_state:
                    st.session_state.user_input = ""
                if "submit_clicked" not in st.session_state:
                    st.session_state.submit_clicked = False
                
                # Create a key for the text input that's different from the session state key
                user_input = st.text_input(
                    "",
                    key="text_input_widget",
                    placeholder="Type your travel question here...",
                    label_visibility="collapsed"
                )
            with col_button:
                send_button = st.button("Send", use_container_width=True, key="send_button")

            # Process user input when send button is clicked or enter is pressed
            if (send_button or user_input) and user_input.strip() and not st.session_state.submit_clicked:
                st.session_state.submit_clicked = True
                st.session_state.user_input = user_input
                
                # Add message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                self.display_message("user", user_input)
                
                # Process the response
                with st.spinner("🤔 Thinking..."):
                    self.process_agent_response(user_input)
                
                st.rerun()
            else:
                st.session_state.submit_clicked = False

        st.markdown('</div>', unsafe_allow_html=True)

    def display_itinerary(self, itinerary_data):
        """Display travel itinerary in a formatted way"""
        st.markdown("### Your Travel Itinerary")
        for date, activities in itinerary_data.items():
            st.markdown(f"**{date}**")
            for activity in activities:
                with st.expander(f"{activity['time']} - {activity['description']}"):
                    st.write(f"🏠 Location: {activity['location']}")
                    if 'notes' in activity:
                        st.write(f"📝 Notes: {activity['notes']}")

    def process_agent_response(self, user_input):
        # Get response from agent
        response = self.agent.run(user_input)

        # Check if response contains itinerary data
        if isinstance(response, dict) and 'itinerary' in response:
            self.display_itinerary(response['itinerary'])
        else:
            # Add message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            self.display_message("assistant", response)

def main():
    from smolagents.agents import MultiStepAgent
    from smolagents.models import LiteLLMModel
    from tools.final_answer import FinalAnswerTool
    from tools.visit_webpage import VisitWebpageTool
    from tools.web_search import DuckDuckGoSearchTool
    from tools.cost_calculator import CostCalculatorTool

    # Initialize tools
    visit_webpage = VisitWebpageTool()
    web_search = DuckDuckGoSearchTool()
    final_answer = FinalAnswerTool()
    cost_calculator = CostCalculatorTool()

    # Initialize the model
    model = LiteLLMModel(
        model_id="gemini/gemini-2.0-flash-exp",
        max_tokens=2096,
        temperature=0.6,
        api_key="AIzaSyDq7dxX4H8bhWokg9NRqY7j999Pw47sQjc"
    )

    # Initialize your agent here with tools and model
    agent = MultiStepAgent(model=model, tools=[visit_webpage, web_search, final_answer])
    ui = StreamlitUI(agent)
    ui.run()

if __name__ == "__main__":
    main()