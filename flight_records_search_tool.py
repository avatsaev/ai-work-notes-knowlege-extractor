from obsidian.obisidan_retriever import get_obsidian_retriever
from langchain.chains import TransformChain
from langchain.agents import Tool
from datetime import datetime

def search_flight_records(keywords) -> dict:

    res = get_obsidian_retriever().get_relevant_documents(" ".join(keywords))
    context = "\n\n --- \n\n".join([r.page_content for r in res])

    return {"flight_records": context}

search_flight_records_chain = TransformChain(input_variables=["keywords"], output_variables=["flight_records"], transform=search_flight_records)


flight_records_search_tool = Tool(
    name="flight_records_search",
    func=search_flight_records_chain.run,
    description="Search for work notes, useful when you need to search for notes about work notes (flight records)"
)


