import requests
import psycopg
import csv
import itertools
import timeit
import threading
from elasticsearch import Elasticsearch, helpers

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "payments"
DB_PASS = "payments"
DB = "payments"

S_HOST = "localhost"
S_PORT = 9200
S_USER = "elastic"
S_PASS = "payments"
S_INDEX = "general-payments"


def generate_search_connection():
    return Elasticsearch(f"http://{S_HOST}:{S_PORT}", basic_auth=(S_USER, S_PASS))


def generate_db_connection():
    conn = psycopg.connect(
        dbname=DB, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS
    )
    return conn


def db_copy_statement(keys):
    joined = ",".join(keys)
    return f"COPY general_payment ({joined}) FROM STDIN"


def start_db_file(file):
    rows = csv.reader(file)
    keys = next(rows)
    return (keys, rows)


def window_iter(iter_, n):
    iters = [iter_] * n
    return (i for i in itertools.zip_longest(*iters))


def read_file_like_bytes_as_csv(file_like):
    """
    Takes a file-like bytes object and creates a csv reader
    that iterates over the object record by record.
    """
    return csv.reader(line.decode() for line in file_like)


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
    dataset = get_dataset(dataset_id)
    url = retrieve_dataset_url(dataset)
    raw_response = stream_dataset_file(url)
    response_lines = read_file_like_bytes_as_csv(raw_response)
    keys = next(response_lines)
    return (keys, response_lines)

def generate_es_index_for_rows(keys, rows):
    id_index = keys.index("Record_ID")
    for row in rows:
        yield {
            "_index": S_INDEX,
            "Record_ID": row[id_index],
            "all": " ".join(itertools.chain(row[:id_index], row[id_index:]))
        }

def copy_csv_to_db(keys, es, db_cursor, copy_statement, rows):
    db_rows, es_rows = itertools.tee(rows)
    print("Copying to db")
    with db_cursor.copy(copy_statement) as copy:
        for row in db_rows:
            copy.write_row(row)
    print("Done copying to db, copying to es")
    for rows_chunk in grouper(1000, es_rows):
        helpers.bulk(es, generate_es_index_for_rows(keys, (row for row in rows_chunk if row)))
    print("Done copying to es")

def grouper(n, iterable):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

def main(dataset_id):
    db_conn = generate_db_connection()
    es_conn = generate_search_connection()
    print("Connected to db and es")
    keys, rows = get_dataset_stream(dataset_id)
    print("Got value stream", keys)
    copy_statement = db_copy_statement(keys)
    print(f"Made copy statement: '{copy_statement}'")
    print(timeit.timeit(lambda: copy_csv_to_db(keys, es_conn, db_conn.cursor(), copy_statement, rows)))


if __name__ == "__main__":
    main("e657f6f0-7abb-5e82-8b42-23bff09f0763")
