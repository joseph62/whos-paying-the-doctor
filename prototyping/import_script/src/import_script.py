import requests
import typer
import csv
import itertools
import datetime
from elasticsearch import Elasticsearch, helpers

S_HOST = "localhost"
S_PORT = 9200
S_USER = "elastic"
S_PASS = "payments"
S_INDEX = "general-payment"


def generate_search_connection():
    return Elasticsearch(f"http://{S_HOST}:{S_PORT}", basic_auth=(S_USER, S_PASS))


def start_db_file(file):
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
    dataset = get_dataset(dataset_id)
    url = retrieve_dataset_url(dataset)
    raw_response = stream_dataset_file(url)
    return raw_response


def generate_es_index_for_rows(keys, rows):
    for row in rows:
        if row:
            src = dict(zip(keys, row))
            src["_all"] = " ".join(row)
            yield {"_index": S_INDEX, "_id": src["Record_ID"], "_source": src}


def grouper(n, iterable):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def copy_file_to_es(file):
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


def main(
    dataset_id: str = typer.Argument(...),
    row_limit: int = typer.Option(..., "--row-limit", "-l"),
):
    make_index_if_not_exists()

    print(datetime.datetime.now())
    raw_stream = get_dataset_stream(dataset_id)

    if row_limit:
        print("limiting row to", row_limit, "lines")
        raw_stream = (row for _, row in zip(range(row_limit), raw_stream))

    copy_file_to_es(raw_stream)

    print(datetime.datetime.now())


if __name__ == "__main__":
    # main("e657f6f0-7abb-5e82-8b42-23bff09f0763")
    typer.run(main)
