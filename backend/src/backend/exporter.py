from xlwt import *

def make_xls_file(out_stream, keys, rows):
    wb = Workbook()
    ws = wb.add_sheet('0')

    for j, k in enumerate(keys):
        ws.write(0, j, k)

    for i, row in enumerate(rows, 1):
        for j, col in enumerate(row):
            ws.write(i, j, col)
    
    wb.save(out_stream)