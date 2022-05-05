import typer
import requests
import csv
import sys


def read_file_like_bytes_as_csv(file_like):
    """
    Takes a file-like bytes object and creates a csv reader
    that iterates over the object record by record.
    """
    return csv.DictReader(line.decode() for line in file_like.readline())


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


def main(
    dataset_id: str = typer.Argument(...),
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "--file", "-f"),
    row_count: int = typer.Option(100, "--row-count", "-c"),
):
    dataset = get_dataset(dataset_id)
    url = retrieve_dataset_url(dataset)
    raw_response = stream_dataset_file(url)
    response_lines = (line for line in raw_response)
    for _, line in zip(range(row_count + 1), response_lines):
        out_file.buffer.write(line)


if __name__ == "__main__":
    typer.run(main)
