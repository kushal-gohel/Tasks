from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.thinking import ThinkingTools
from agno.tools.yfinance import YFinanceTools
import os 
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY_temp")

thinking_agent = Agent(
        model=Groq(id="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY),    
        tools=[ ThinkingTools(add_instructions=True),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
    ],
    instructions="Use tables where possible",
    show_tool_calls=True,
    markdown=True,
)

result = thinking_agent.print_response("Write a report comparing NVDA to TSLA", stream=True)

print(result)