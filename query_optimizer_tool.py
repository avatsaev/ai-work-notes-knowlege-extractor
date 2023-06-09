from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.prompts import PromptTemplate

load_dotenv()
from langchain import OpenAI, LLMChain
import os
from datetime import datetime

template = """Assume that today's date is {today_date}. Your goal is to optimize a user search query for a search engine. 
The query may contain dates tags and urls.
tags: review, bug, pair, sprint, pr, sprint, 1:1, pull request = pr
query optimization process: 
 - if there is any temporal elements transform the query to include precise dates
    for example "what did I do this week" -> "what did I do between 2021-01-01, 2021-01-07"
 - if the query does not have any temporal elements, dont change it
 - make sure the words similar to tags are transformed into the tags
    for example "how many pull request did I submit" -> "how many pr did I submit"
 
keyword categories:
- https links and urls 
- dates
- names 
- ticket numbers from queries, like: "PIMS-1234", 
- tags, 

output: extract the keywords from the optimized query, and return the optimized query as well as extracted keywords in a json format (optimized query key: 'optimized_query', keywords key: 'keywords').

user query: {query}
"""

flight_record_query_optimizer_template = PromptTemplate(
    input_variables=["query", "today_date"],
    template=template
)

llm = OpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_KEY"),
)

flight_records_query_optimizer_chain = LLMChain(
    prompt=flight_record_query_optimizer_template,
    llm=llm,
    verbose=True
)


query_optimizer_tool = Tool(
    name="query_optimizer",
    func=flight_records_query_optimizer_chain.run,
    description="Optimize a user flight records search query, useful when you need to optimize query to search in work notes"
)
# query = "what did I do last month"
#
# res = flight_records_query_optimizer_chain.predict(query=query, today_date=datetime.today().strftime('%d-%m-%Y'))
#
# print(res)
