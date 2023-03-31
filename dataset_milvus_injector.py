from dataset_extractor import extract_dataset_records, create_flight_record_collection_item
from milvus_service import init_db_connection, insert_flight_records, get_flight_records_collection, reset_flight_records_collection, init_flight_records_collection
from splitter import extract_flight_records
import os

def encode_records_for_insertion(records):
    output_list = []

    for key in records[0].keys():
        values = [d[key] for d in records]
        output_list.append(values)

    return output_list

def flight_records_dataset_is_empty():
    if os.path.exists("datasets/flight-records"):
        if not os.listdir("datasets/flight-records"):
            return True
        else:
            return False
    else:
        return True


def inject_data_into_milvus():

    if flight_records_dataset_is_empty():
        extract_flight_records("fl.md")

    flight_records = extract_dataset_records("datasets/flight-records")
    # print(flight_records)

    init_db_connection()
    init_flight_records_collection()

    formatted_records = []
    for sample in flight_records:
        # this operation costs money
        formatted_records.append(
            create_flight_record_collection_item(sample)
        )

    encoded_records = encode_records_for_insertion(formatted_records)
    # print(encoded_records)
    res = insert_flight_records(encoded_records)
    get_flight_records_collection().flush()
    # print(res)

#
# init_db_connection()
# reset_flight_records_collection()
# init_flight_records_collection()
# inject_data_into_milvus()
#

