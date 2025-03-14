from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

import os
from dotenv import load_dotenv
load_dotenv()

# os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY_2"]=os.getenv("GROQ_API_KEY_2")

web_agent=Agent(
    model=Groq(id="qwen-2.5-32b"),
    name="Web Agent",
    role="SEarch the web for information",
    tools=[DuckDuckGoTools()],
    instructions=["Always provide the sources "],
    show_tool_calls=True,
    markdown=True
    )
finagent = Agent(
    model=Groq(id="deepseek-r1-distill-qwen-32b"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    # show_tool_calls=True,
    description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
    instructions=["Format your response using markdown and use tables to display data where possible."],
    show_tool_calls=True,
    markdown=True
)
team=Agent(
    team=[web_agent,finagent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Always provide the sources ","Use tables to show data"],
    show_tool_calls=True,
    markdown=True
)



team.print_response(" i have 1000 inr to invest in stocks and i am looking for long term investment oppurtunities in the tech sector. Can you provide me with a list of stocks that i can invest in INDIA ?")






















# agent=Agent(
#     model=Groq(id="qwen-2.5-32b"),
#     description="You are an assistant please reply based ont he question",
#     tools=[DuckDuckGoTools()],
#     markdown=True
# )

# agent.print_response("Who won the India vs Pakistan  in CWC 2003?")