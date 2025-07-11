from agno.agent import Agent
from agno.models.groq import Groq
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.storage.agent.sqlite import SqliteAgentStorage
import os
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model=Groq(id="llama3-8b-8192"),
    storage=SqliteAgentStorage(
        table_name = "storage_agent",
        db_file = 'storage/agent_storage.db'
    ),
    add_history_to_messages=True,
    session_id="5375abc1-857a-4821-b00c-85361ac07dff"
)

# agent.print_response("My name is Kushal")
# agent.print_response("I live in Ahmedabad.")
# agent.print_response("I am an AI/ML engineer.")
# agent.print_response("I love to work in the field of AI and Machine Learning.")
# agent.print_response("If I were to be a podcaster, I would be a tech podcaster.")
agent.print_response("Can you give a brief summary of my interests and profession?")

