from langchain import PromptTemplate

template = """Today's date is {today_date}. You're an ai assistant that helps the user with their notes taken at work everyday. 
Each note starts with a date followed by hashtags. Answer the question based on the notes below, list links related to the question after the answer. 
If the question cannot be answered using the information provided answer with "I don't know". Dont answer questions outside the scope of the notes.
Cite your sources at the end of the answer.

Notes:
{flight_records}

"""

flight_records_system_prompt_template = PromptTemplate(
    input_variables=["today_date", "flight_records"],
    template=template
)