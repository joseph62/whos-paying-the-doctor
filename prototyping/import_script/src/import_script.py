import requests
import psycopg
from psycopg import sql
import csv
import itertools
import timeit

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
    return None


def generate_db_connection():
    conn = psycopg.connect(
        dbname=DB, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS
    )
    conn.autocommit = True
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


def copy_csv_to_db(copy, rows):
    for row in rows:
        copy.write_row(row)


def main(dataset_id):
    db_conn = generate_db_connection()
    print("Connected to db")
    cursor = db_conn.cursor()
    keys, value_lines = get_dataset_stream(dataset_id)
    print("Got value stream", keys)
    copy_statement = db_copy_statement(keys)
    print(f"Made copy statement: '{copy_statement}'")
    print("Starting copy")
    with cursor.copy(copy_statement) as copy:
        print(timeit.timeit(lambda: copy_csv_to_db(copy, value_lines)))
    print("Copy done")


if __name__ == "__main__":
    main("e657f6f0-7abb-5e82-8b42-23bff09f0763")
