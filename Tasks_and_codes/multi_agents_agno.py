from agno.agent import Agent #type:ignore
from agno.models.groq import Groq #type:ignore
from agno.tools.duckduckgo import DuckDuckGoTools #type:ignore
from agno.tools.yfinance import YFinanceTools   #type:ignore

import os
from dotenv import load_dotenv #type:ignore
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

web_agent = Agent(
    name = "Web Search Agent",
    role = "Search the web for information and answer the questions",
    model=Groq(id="gemma2-9b-it"),
    tools=[DuckDuckGoTools()],
    instructions= "Always include the source of the information you provide.",
    show_tool_calls= True,
    markdown=True
)

finance_agent = Agent(
    name = "Finance Agent",
    role = "Answer questions related to finance and stock prices.",
    model=Groq(id="meta-llama/llama-4-maverick-17b-128e-instruct"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    instructions= "Use tables to display data. After analyzing the companies, provide a clear recommendation on which company to buy for the long term, along with detailed reasoning based on the financial data and future prospects.",
    show_tool_calls= True,
    markdown=True
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="gemma2-9b-it"),
    instructions="You are a team of agents. Use the tools provided to answer questions about web searches and financial data",
    show_tool_calls=True,
    markdown=True
    )

response = agent_team.run(
    "Analyze companies like Apple, Tesla, and Microsoft and suggest which to buy for the long term?",
    stream=False
)

print(response.content)
