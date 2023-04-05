from langchain.agents import Tool
from datetime import datetime
from langchain.chains import TransformChain


search_flight_records_chain = TransformChain(input_variables=["query"], output_variables=["flight_records"], transform=lambda _:  datetime.today().strftime('%d-%m-%Y'))



today_date_tool = Tool(
    name="today_date",
    func=search_flight_records_chain.run,
    description="Get today's date"

)