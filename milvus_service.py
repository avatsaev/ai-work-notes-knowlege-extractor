from pymilvus import connections

from pymilvus import CollectionSchema, FieldSchema, DataType, Collection, utility

connection = None


def init_db_connection():
    global connection
    connection = connections.connect(
        alias="default",
        host='localhost',
        port='19530'
    )
    return connection


def delete_flight_records_collection(collection_name='flight_records'):
    print("Deleting flight_records collection...")
    # Delete collection
    try:
        collection = Collection(name=collection_name, using='default')
        collection.drop()
    except:
        print("Collection does not exist")


# get collection by name
def get_flight_records_collection(collection_name='flight_records'):
    collection = Collection(name=collection_name, using='default')
    return collection

def load_flight_records_collection():
    collection = get_flight_records_collection()
    collection.load()
    return collection

def has_collection(name):
    return utility.has_collection(name)


def init_flight_records_collection():
    if not has_collection('flight_records'):
        print("Creating flight_records collection...")
        flight_record_id = FieldSchema(
            name="flight_record_id",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True
        )
        flight_record_tags = FieldSchema(
            name="flight_record_tags",
            dtype=DataType.VARCHAR,
            max_length=200,
        )
        flight_record_date = FieldSchema(
            name="flight_record_date",
            dtype=DataType.VARCHAR,
            max_length=20,
        )
        flight_record_contents = FieldSchema(
            name="flight_record_contents",
            dtype=DataType.VARCHAR,
            max_length=3500,
        )
        flight_record_contents_embed = FieldSchema(
            name="flight_record_contents_embed",
            dtype=DataType.FLOAT_VECTOR,
            dim=1536
        )
        schema = CollectionSchema(
            fields=[flight_record_id, flight_record_tags, flight_record_date, flight_record_contents, flight_record_contents_embed],
            description="flight records search"
        )

        # Create collection
        collection = Collection(
            name='flight_records',
            schema=schema,
            using='default',
        )
        build_flight_records_index()
        return collection
    else:
        print("Collection flight_records already exists")
        return get_flight_records_collection()


def build_flight_records_index():
    collection = get_flight_records_collection()
    print('building indexes...')
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1024}
    }
    collection.create_index(field_name='flight_record_contents_embed', index_params=index_params)
    collection.create_index(field_name='flight_record_tags')
    collection.create_index(field_name='flight_record_contents')
    collection.create_index(field_name='flight_record_date')

def reset_flight_records_collection():
    init_db_connection()
    delete_flight_records_collection()
    init_flight_records_collection()

# insert a flight record into the collection input param flight record is a python hash
def insert_flight_records( flight_records):
    collection = get_flight_records_collection()
    ids = collection.insert(flight_records)
    return ids


def get_flight_records_by_ids(ids):
    load_flight_records_collection()
    collection = get_flight_records_collection()
    res = collection.query(
        expr='flight_record_id in [{}]'.format(','.join([str(id) for id in ids])),
        output_fields=['flight_record_id', 'flight_record_tags', 'flight_record_date', 'flight_record_contents'],
        consostensy_level='Strong',
    )
    collection.release()
    return res

def vector_search_flight_records(query_vector, top_k=5):
    load_flight_records_collection()
    collection = get_flight_records_collection()
    output_fields = ['flight_record_id']
    res = collection.search(
        data=[query_vector],
        anns_field="flight_record_contents_embed",
        param={'metric_type': 'L2', 'params': {'nprobe': 16}},
        limit=top_k,
        output_fields=output_fields,
    )
    collection.release()
    return res


# if __name__ == '__main__':
#
#     init_db_connection()
#     delete_flight_records_collection('flight_records')
#     # init_flight_records_collection()
#     # col = init_flight_records_collection()
#     #
#     # print( col)
#     # build_flight_records_index()
#     # reset_flight_records_collection()
#
