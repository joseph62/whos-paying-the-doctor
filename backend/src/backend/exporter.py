from xlwt import *


def make_xls_file(out_stream, rows):
    wb = Workbook()
    ws = wb.add_sheet("0")

    try:
        first = next(rows)
        keys = [k for k in first.keys() if k != "_all"]

        for j, k in enumerate(keys):
            ws.write(0, j, k)
            ws.write(1, j, first[k])

        for i, row in enumerate(rows, 2):
            for j, key in enumerate(keys):
                ws.write(i, j, row[key])
    except StopIteration:
        pass

    wb.save(out_stream)
