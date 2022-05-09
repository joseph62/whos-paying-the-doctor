import os
import psycopg
import elasticsearch

DB_NAME = os.environ.get("DB_NAME", "payments")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", 5432)
DB_USER = os.environ.get("DB_USER", "payments")
DB_PASS = os.environ.get("DB_PASS", "payments")

def get_db_connection():
    conn = psycopg.connect(
        dbname=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, autocommit=True, sslmode="disable"
    )
    return conn


ES_HOST = os.environ.get("ES_HOST", "search")
ES_PROTOCOL = os.environ.get("ES_PROTOCOL", "http")
ES_PORT = os.environ.get("ES_PORT", 9200)
ES_USER = os.environ.get("ES_USER", "elastic")
ES_PASS = os.environ.get("ES_PASS", "payments")
ES_INDEX = os.environ.get("ES_INDEX", "general-payment")

def get_search_connection():
    return elasticsearch.Elasticsearch(f"{ES_PROTOCOL}://{ES_HOST}:{ES_PORT}", basic_auth=(ES_USER, ES_PASS))

