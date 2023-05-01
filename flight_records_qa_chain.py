from langchain.chains import RetrievalQA
from obsidian.obisidan_retriever import get_obsidian_retriever
from llm.gpt4all import get_gpt4all_llm
from flight_records_prompt_template import flight_records_prompt_template

llm = get_gpt4all_llm()

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
