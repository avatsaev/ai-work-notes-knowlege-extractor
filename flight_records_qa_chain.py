from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from query_optimizer_tool import query_optimizer_tool
from flight_records_search_tool import flight_records_search_tool
import os
from dotenv import load_dotenv
from flight_records_assistant_tool import flight_records_tool
from today_date_tool import today_date_tool
from langchain.chains import RetrievalQA
from obsidian.obisidan_retriever import get_obsidian_retriever

from flight_records_prompt_template import flight_records_prompt_template
load_dotenv()

tools = [query_optimizer_tool, flight_records_search_tool, flight_records_tool, today_date_tool]
llm = OpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_KEY")
)
flight_records_agent = initialize_agent(tools, llm, agent='zero-shot-react-description', verbose=True)

PROMPT = flight_records_prompt_template
chain_type_kwargs = {"prompt": PROMPT}

flight_records_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=get_obsidian_retriever(),
    chain_type_kwargs=chain_type_kwargs,
    verbose=True
)



if __name__ == '__main__':

    print("\nWelcome to the flight records assistant. Ask me anything about your flight records. I'll try to answer your questions.\n")
    while True:

        print("\n----------------------------\n")
        query = input("Query your flight records: ")
        # flight_records_agent.run(query)
        res = flight_records_qa_chain.run(query)
        print(res)
