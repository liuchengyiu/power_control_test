import codecs
def record(result):
    for joins in result:
        write_file(str(joins.get('type'))+ ','+ str(joins.get('message'))+ ','+ str(joins.get('flag'))+ '\r\n')


def write_file(read):
    f = codecs.open("result_log.txt", "a", 'utf-8')
    f.write(read)
