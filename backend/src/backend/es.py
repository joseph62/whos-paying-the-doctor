from .connections import ES_INDEX

def make_query(terms):
    return {
        "multi_match": {
        "query": terms,
        "type": "bool_prefix",
        "fields": [
            "all",
            "all._2gram",
            "all._3gram"
        ]
    }}

def get_search_suggestions(es_conn, terms):
    response = es_conn.search(index=ES_INDEX, size=20, query=make_query(terms))
    hits = response.get('hits', {}).get('hits', [])
    return [h['_source']['all'] for h in hits if h and '_source' in h and 'all' in h['_source']]

def get_search_results(es_conn, terms, size):
    response = es_conn.search(index=ES_INDEX, size=size, query=make_query(terms))
    hits = response.get('hits', {}).get('hits', [])
    return (h['_source'] for h in hits if '_source' in h)