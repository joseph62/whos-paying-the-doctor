from . import connections, exporter, es
import io
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/suggestions")
async def search_suggestions(response: Response, terms: str):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return es.get_search_suggestions(connections.get_search_connection(), terms)


@app.get("/search-results")
async def search(response: Response, terms: str, size: int = 100):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return es.get_search_results(connections.get_search_connection(), terms, size)


@app.get("/search-results/xls")
async def export_search(response: Response, terms: str):
    rows = es.get_search_results(connections.get_search_connection(), terms, 10000)
    stream = io.BytesIO()
    exporter.make_xls_file(stream, rows)
    stream.seek(0)
    file_name_suffix = terms.replace(" ", "_").replace('"', "")[:50]
    response = StreamingResponse(stream)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers[
        "Content-Disposition"
    ] = f'attachement; filename="2015GP_{file_name_suffix}.xls"'
    return response
