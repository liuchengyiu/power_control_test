def record(result):
    for joins in result:
        write_file(str(joins.get('type'))+ ','+ str(joins.get('message'))+ ','+ str(joins.get('flag'))+ '\r\n')


def write_file(read):
    f = open("result_log.txt", "a")
    f.write(read)
