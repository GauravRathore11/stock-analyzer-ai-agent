from google.adk.agents.llm_agent import Agent
from stock_agent.prompts import system_instruction, description
from stock_agent.tools import get_stock_price, get_historical_data, get_stock_fundamentals

root_agent = Agent(
    model = 'gemini-2.5-flash',
    name = 'root_agent',
    description = description,
    instruction = system_instruction,
    tools=[get_stock_price, get_historical_data, get_stock_fundamentals]
)