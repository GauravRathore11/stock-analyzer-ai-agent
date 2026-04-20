from google.adk.agents.llm_agent import Agent
from stock_agent.prompts import system_instruction, description
from stock_agent.tools import get_stock_price, get_historical_data, get_stock_fundamentals
from google.adk.models.lite_llm import LiteLlm

local_model = LiteLlm(model="ollama_chat/qwen2.5:0.5b")

root_agent = Agent(
    model = local_model,
    name = 'root_agent',
    description = description,
    instruction = system_instruction,
    tools=[get_stock_price, get_historical_data, get_stock_fundamentals]
)