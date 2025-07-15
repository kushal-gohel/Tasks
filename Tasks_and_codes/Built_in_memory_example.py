from agno.agent import Agent
from agno.models.groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY_temp_1")

# === Initialize Agent ===
agent = Agent(
    model=Groq(id="llama3-8b-8192"),
        add_history_to_messages=True,
        num_history_responses=3,
        markdown=True
)

agent.print_response("My name is Kushal")
agent.print_response("I live in Ahmedabad.")
agent.print_response("What is my name?")