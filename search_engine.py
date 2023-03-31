from milvus_service import vector_search_flight_records, get_flight_records_by_ids, init_db_connection
from embedder import openai_embed


def query_flight_records(query, top_k=10):
    print(f"Querying flight records with keywords: {query}")
    init_db_connection()
    search_vector = openai_embed(query)
    search_results = vector_search_flight_records(search_vector, top_k)

    ids = [result.id for result in search_results[0]]
    result_records = get_flight_records_by_ids(ids)
    # print(result_records)
    return result_records

#
# res = query_flight_records("https://doctolib.atlassian.net")
# print(res)
#
