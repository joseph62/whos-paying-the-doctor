import itertools
import datetime
import requests
import csv
import os

from elasticsearch import Elasticsearch, helpers

S_PROTOCOL = os.environ.get("ES_PROTOCOL", "http")
S_HOST = os.environ.get("ES_HOST", "search")
S_PORT = os.environ.get("ES_PORT", "9200")
S_USER = os.environ.get("ES_USER", "elastic")
S_PASS = os.environ.get("ES_PASS", "payments")
S_INDEX = os.environ.get("ES_INDEX", "general-payment")

DO_FULL_IMPORT = os.environ.get("IMPORT_TYPE", "update") == "full"
IMPORT_LIMIT = int(os.environ.get("IMPORT_LIMIT", "100000"))
IMPORT_DATA_SET_ID = "e657f6f0-7abb-5e82-8b42-23bff09f0763"

def generate_search_connection():
    """
    Create Elasticsearch connections based on environment variables
    """
    return Elasticsearch(f"{S_PROTOCOL}://{S_HOST}:{S_PORT}", basic_auth=(S_USER, S_PASS))


def start_db_file(file):
    """
    Wrap byte file like iterator in a csv reader return a tuple of the head of the lines
    as the keys line and the remaining iterator as the second element of the tuple
    """
    rows = csv.reader(row.decode() for row in file)
    keys = next(rows)
    return (keys, rows)


def get_dataset(dataset_id):
    """
    Requests metadata for the provided dataset id.

    Raises error if request returns 4XX or 5XX status
    otherwise returns parsed Open Payments dataset metadata response.
    """
    response = requests.get(
        f"https://openpaymentsdata.cms.gov/api/1/metastore/schemas/dataset/items/{dataset_id}",
        headers={"accept": "application/json"},
    )
    response.raise_for_status()
    return response.json()


def stream_dataset_file(dataset_download_url):
    """
    Begins request for dataset download.

    Raises error if request returns 4XX or 5XX
    otherwise returns a file-like object that the response can be read from
    """
    response = requests.get(dataset_download_url, stream=True)
    response.raise_for_status()
    return response.raw


def retrieve_dataset_url(dataset):
    """
    Given an Open Payments dataset metadata object find a download url

    raises ValueError if there is no distrubtion or no download url for the first distrubtion
    returns url
    """
    distributions = dataset.get("distribution", [])
    if not distributions:
        raise ValueError("Dataset did not have distrubtions")
    url = distributions[0].get("downloadURL")
    if not url:
        raise ValueError("Distrubtion of dataset did not have a download url")
    return url


def get_dataset_stream(dataset_id):
    """
    Given an Open Payments dataset id retrieve the dataset raw bytes
    """
    dataset = get_dataset(dataset_id)
    url = retrieve_dataset_url(dataset)
    raw_response = stream_dataset_file(url)
    return raw_response


def generate_es_index_for_rows(keys, rows):
    """
    Generate elastic search index request models for each row in the rows iterator
    """
    for row in rows:
        if row:
            src = dict(zip(keys, row))
            if not DO_FULL_IMPORT and src["Change_Type"] == "UNCHANGED":
                continue
            src["_all"] = " ".join(row)
            yield {"_index": S_INDEX, "_id": src["Record_ID"], "_source": src}


def grouper(n, iterable):
    """
    Turn iterable into iterable chunks of length n
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def copy_file_to_es(file):
    """
    Given a byte file like iterable read rows and index records into elasticsearch 
    """
    es_conn = generate_search_connection()
    print("Connected to ES server")
    keys, rows = start_db_file(file)
    for rows_chunk in grouper(1000, rows):
        helpers.bulk(
            es_conn,
            generate_es_index_for_rows(keys, (row for row in rows_chunk if row)),
        )
    print("Done indexing es server")


def make_index_if_not_exists():
    """
    Connect to Elasticsearch and create the general-payment index with
    a search_as_you_type field for typeahead
    """
    es_conn = generate_search_connection()
    if not es_conn.indices.exists(index=S_INDEX).body:
        es_conn.indices.create(
            index=S_INDEX,
            body={
                "settings": {},
                "mappings": {
                    "properties": {
                        "Record_ID": {"type": "keyword"},
                        "_all": {"type": "search_as_you_type"},
                    }
                },
            },
        )


def main():
    make_index_if_not_exists()

    print(datetime.datetime.now())
    raw_stream = get_dataset_stream(IMPORT_DATA_SET_ID)

    if IMPORT_LIMIT:
        print("limiting row to", IMPORT_LIMIT, "lines")
        raw_stream = (row for _, row in zip(range(IMPORT_LIMIT), raw_stream))

    copy_file_to_es(raw_stream)

    print(datetime.datetime.now())


if __name__ == "__main__":
    main()
