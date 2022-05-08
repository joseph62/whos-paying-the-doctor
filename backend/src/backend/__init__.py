import logging
import os
from fastapi import FastAPI, Response

DB_NAME = os.environ.get("DB_NAME", "payments")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", 5432)
DB_USER = os.environ.get("DB_USER", "payments")
DB_PASS = os.environ.get("DB_PASS", "payments")

logging.info(
    f"Using database properties: {DB_NAME=} {DB_HOST=} {DB_PORT=} {DB_USER=} {DB_PASS=}"
)


ES_HOST = os.environ.get("ES_HOST", "search")
ES_PROTOCOL = os.environ.get("ES_PROTOCOL", "http")
ES_PORT = os.environ.get("ES_PORT", 9200)
ES_USER = os.environ.get("ES_USER", "elastic")
ES_PASS = os.environ.get("ES_PASS", "payments")
ES_INDEX = os.environ.get("ES_INDEX", "general-payments")

logging.info(
    f" Using search properties: {ES_HOST=} {ES_PROTOCOL=} {ES_PORT=} {ES_USER=} {ES_PASS=} {ES_INDEX=}"
)


app = FastAPI()


@app.get("/suggestions")
async def search_suggestions(response: Response, terms: str):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return list(f"{terms} {i}" for i in range(5))

@app.get("/search-results")
async def search(response: Response, terms: str):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return [{"Record_ID": i, "all": f"{terms} {i}"} for i in range(500)]


@app.get("/search-results/xls")
async def export_search(response: Response, terms: str):
    file_name_suffix = terms.replace(" ", "_").replace('"', "")[:50]
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Disposition'] = f'attachement; filename="2015GP_{file_name_suffix}.xls"'
    return """
    This is a very cool XLS file
    """
