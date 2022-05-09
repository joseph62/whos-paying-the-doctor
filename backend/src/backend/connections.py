import os
import elasticsearch


ES_HOST = os.environ.get("ES_HOST", "search")
ES_PROTOCOL = os.environ.get("ES_PROTOCOL", "http")
ES_PORT = os.environ.get("ES_PORT", 9200)
ES_USER = os.environ.get("ES_USER", "elastic")
ES_PASS = os.environ.get("ES_PASS", "payments")
ES_INDEX = os.environ.get("ES_INDEX", "general-payment")

def get_search_connection():
    return elasticsearch.Elasticsearch(f"{ES_PROTOCOL}://{ES_HOST}:{ES_PORT}", basic_auth=(ES_USER, ES_PASS))

