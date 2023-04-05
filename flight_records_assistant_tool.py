from flight_records_prompt_template import flight_records_system_prompt_template
from langchain.agents import Tool
from langchain import OpenAI, LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_KEY"),
)

flight_records_query_optimizer_chain = LLMChain(prompt=flight_records_system_prompt_template, llm=llm, verbose=False)


flight_records_tool = Tool(
    name="work_notes_assistant_tool",
    func=flight_records_query_optimizer_chain.run,
    description="Useful when you need to analyze and answer questions about user's work notes (flight records). Input must be user's work notes (flight records) and today's date"
)

