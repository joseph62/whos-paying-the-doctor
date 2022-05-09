import requests
import typer
import psycopg
import csv
import itertools
import datetime
import multiprocessing
import os
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
S_INDEX = "general-payment"


def generate_search_connection():
    return Elasticsearch(f"http://{S_HOST}:{S_PORT}", basic_auth=(S_USER, S_PASS))


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
    return raw_response

def generate_es_index_for_rows(keys, rows):
    id_index = keys.index("Record_ID")
    for row in rows:
        if row:
            yield {
                "_index": S_INDEX,
                "_id": row[id_index],
                "_source": {
                    "Record_ID": row[id_index],
                    "all": " ".join(row)
                }
            }

def grouper(n, iterable):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

def copy_file_to_db(file_name):
    db_conn = generate_db_connection()
    print("Connected to db")
    with open(file_name) as f:
        keys, rows = start_db_file(f)
        statement = db_copy_statement(keys)
        print("Starting copy from file to db")
        for row_chunk in grouper(1000, rows):
            with db_conn.cursor().copy(statement) as copy:
                for row in filter(lambda r: len(r) == len(keys), (row for row in row_chunk if row)):
                    copy.write_row(row)
    print("DB copy complete")

def copy_file_to_es(file_name):
    es_conn = generate_search_connection()
    print("Connected to ES server")
    with open(file_name) as f:
        keys, rows = start_db_file(f)
        for rows_chunk in grouper(1000, rows):
            helpers.bulk(es_conn, generate_es_index_for_rows(keys, (row for row in rows_chunk if row)))
    es_conn.indices.refresh(index=S_INDEX)
    print("Done indexing es server")

def make_index_if_not_exists():
    es_conn = generate_search_connection()
    if not es_conn.indices.exists(index=S_INDEX).body:
        es_conn.indices.create(index=S_INDEX, body={
    "settings": {},
    "mappings": {
        "properties": {
        "Record_ID": { "type": "keyword" },
        "all": { "type": "search_as_you_type" }
        }
    }
    })

def truncate_data_table():
    db = generate_db_connection()
    db.cursor().execute("""
    TRUNCATE general_payment;
    """)

def main(
    dataset_id: str = typer.Argument(...),
    row_limit: int = typer.Option(..., "--row-limit", "-l"),
):
    make_index_if_not_exists()
    truncate_data_table()

    print(datetime.datetime.now())
    file_name = f"{dataset_id}.csv"

    if not os.path.exists(file_name):
        raw_stream = get_dataset_stream(dataset_id)
        if row_limit:
            print("limiting row to", row_limit, "lines")
            raw_stream = (row for _, row in zip(range(row_limit), raw_stream))
        with open(file_name, 'w') as f:
            for line in raw_stream:
                f.buffer.write(line)
    else:
        print("File already exists, skipping download")

    db_p = multiprocessing.Process(target=copy_file_to_db, args=(file_name,))
    es_p = multiprocessing.Process(target=copy_file_to_es, args=(file_name,))
    db_p.start()
    es_p.start()
    db_p.join()
    es_p.join()
    print(datetime.datetime.now())


if __name__ == "__main__":
    #main("e657f6f0-7abb-5e82-8b42-23bff09f0763")
    typer.run(main)
