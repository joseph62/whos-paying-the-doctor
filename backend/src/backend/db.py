import itertools

def grouper(n, iterable):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

def make_select_by_ids_statement(num_ids):
    id_params = ",".join(["%s"]*num_ids)
    return f"""
    SELECT * FROM general_payment
    WHERE record_id IN ({id_params});
    """

def get_rows_by_ids(db_conn, row_ids):
    keys = []
    for rows_chunk in grouper(100, row_ids):
        ids = [r for r in rows_chunk if r]
        cursor = db_conn.cursor().execute(make_select_by_ids_statement(len(ids)), ids)
        if not keys:
            keys = [col.name for col in cursor.description]
            yield keys
        yield from cursor.fetchall()
        
        