from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from obsidian.obisidan_retriever import get_obsidian_retriever
from query_optimizer_tool import flight_records_query_optimizer_chain
from flight_records_prompt_template import flight_records_system_prompt_template
from langchain.schema import (
    SystemMessage,
    HumanMessage,
)

import json

from datetime import datetime


load_dotenv()
obsidian_retriever = get_obsidian_retriever()

chat_openai = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_KEY"),
    model_name='gpt-3.5-turbo',  # can be used with llms like 'gpt-3.5-turbo'
    verbose=True,
)

if __name__ == '__main__':

    print("\nWelcome to the flight records assistant. Ask me anything about your flight records. I'll try to answer your questions.\n")
    while True:

        print("\n----------------------------\n")
        query = input("Query your flight records: ")
        today_date = datetime.today().strftime('%d-%m-%Y')

        optimized_query_res = flight_records_query_optimizer_chain.predict(query=query, today_date=today_date)
        optimized_query_json = json.loads(optimized_query_res)
        optimized_query = optimized_query_json['optimized_query']
        keywords = optimized_query_json['keywords']

        print(optimized_query_res)
        print(f"Original query: {query}")
        print(f"Optimized query: {optimized_query}")
        print(f"Keywords: {keywords}")

        res = obsidian_retriever.get_relevant_documents(" ".join(keywords))

        context = "\n\n --- \n\n".join([r.page_content for r in res])


        system_prompt = flight_records_system_prompt_template.format(
            today_date=today_date,
            flight_records=context,
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ]

        chat_res = chat_openai(messages)

        print("\n")
        print(chat_res.content)


    #
    # out = count_tokens(
    #     conversation_mem,
    #     prompt_template.format(
    #         query="Which libraries and model providers offer LLMs?"
    #     )
    # )
    #


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
